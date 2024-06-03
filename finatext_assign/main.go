package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"net/http"
	"os"
	"strconv"
	"strings"

	_ "github.com/go-sql-driver/mysql"
)

type ExternalAPIResponse struct {
	Response struct {
		Location []struct {
			City       string `json:"city"`
			Town       string `json:"town"`
			X          string `json:"x"`
			Y          string `json:"y"`
			Prefecture string `json:"prefecture"`
			Postal     string `json:"postal"`
		} `json:"location"`
	} `json:"response"`
}

type AddressResponse struct {
	PostalCode       string  `json:"postal_code"`
	HitCount         int     `json:"hit_count"`
	Address          string  `json:"address"`
	TokyoStaDistance float64 `json:"tokyo_sta_distance"`
}

type AccessLogCount struct {
	PostalCode   string `json:"postal_code"`
	RequestCount int    `json:"request_count"`
}

func getAddressFromPostalCode(w http.ResponseWriter, r *http.Request) {
	postalCode := r.URL.Query().Get("postal_code")
	if len(postalCode) != 7 {
		http.Error(w, "Invalid postal code", http.StatusBadRequest)
		return
	}

	externalAPIUrl := fmt.Sprintf("https://geoapi.heartrails.com/api/json?method=searchByPostal&postal=%s", postalCode)
	resp, err := http.Get(externalAPIUrl)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	var externalAPIResponse ExternalAPIResponse
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	err = json.Unmarshal(body, &externalAPIResponse)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var addressParts []string
	tokyoStaLat, tokyoStaLon := 35.6809591, 139.7673068
	var maxDistance float64
	for _, location := range externalAPIResponse.Response.Location {
		addressParts = append(addressParts, location.Prefecture, location.City, location.Town)
		lat, _ := strconv.ParseFloat(location.Y, 64)
		lon, _ := strconv.ParseFloat(location.X, 64)
		distance := calcDistance(lat, lon, tokyoStaLat, tokyoStaLon)
		if distance > maxDistance {
			maxDistance = distance
		}
	}

	address := strings.Join(removeEmpty(addressParts), "")
	addressResponse := AddressResponse{
		PostalCode:       postalCode,
		HitCount:         len(externalAPIResponse.Response.Location),
		Address:          address,
		TokyoStaDistance: round(maxDistance, 1),
	}

	// アクセスログをデータベースに保存
	db, err := getDBConnection()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer db.Close()
	_, err = db.Exec("INSERT INTO access_logs (postal_code) VALUES (?)", postalCode)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	jsonResponse, err := json.Marshal(addressResponse)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonResponse)
}

func getAccessLogCounts(w http.ResponseWriter, r *http.Request) {
	db, err := getDBConnection()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer db.Close()

	rows, err := db.Query("SELECT postal_code, COUNT(*) AS request_count FROM access_logs GROUP BY postal_code ORDER BY request_count DESC")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var counts []AccessLogCount
	for rows.Next() {
		var count AccessLogCount
		err = rows.Scan(&count.PostalCode, &count.RequestCount)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		counts = append(counts, count)
	}

	jsonResponse, err := json.Marshal(map[string][]AccessLogCount{"access_logs": counts})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonResponse)
}

func getDBConnection() (*sql.DB, error) {
	dbHost := os.Getenv("MYSQL_HOST")
	dbPort := os.Getenv("MYSQL_PORT")
	dbUser := os.Getenv("MYSQL_USER")
	dbPassword := os.Getenv("MYSQL_PASSWORD")
	dbName := os.Getenv("MYSQL_DATABASE")

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", dbUser, dbPassword, dbHost, dbPort, dbName)
	return sql.Open("mysql", dsn)
}

func calcDistance(lat1, lon1, lat2, lon2 float64) float64 {
	const R = 6371.0

	lat1Rad := lat1 * math.Pi / 180
	lon1Rad := lon1 * math.Pi / 180
	lat2Rad := lat2 * math.Pi / 180
	lon2Rad := lon2 * math.Pi / 180

	dlon := lon2Rad - lon1Rad
	dlat := lat2Rad - lat1Rad

	a := math.Pow(math.Sin(dlat/2), 2) + math.Cos(lat1Rad)*math.Cos(lat2Rad)*math.Pow(math.Sin(dlon/2), 2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))

	return R * c
}

func round(val float64, places int) float64 {
	mult := math.Pow(10, float64(places))
	return math.Round(val*mult) / mult
}

func removeEmpty(strs []string) []string {
	var result []string
	for _, str := range strs {
		if str != "" {
			result = append(result, str)
		}
	}
	return result
}

func main() {
	http.HandleFunc("/address", getAddressFromPostalCode)
	http.HandleFunc("/address/access_logs", getAccessLogCounts)
	fmt.Println("Server listening on http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}
