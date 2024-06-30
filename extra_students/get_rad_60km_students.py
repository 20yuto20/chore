import pandas as pd
from geopy.distance import geodesic

# Load the required data
uni_coords = pd.read_csv('/Users/yutokohata/Desktop/chores/extra_students/uni_coord.csv', sep='\t')
student_info = pd.read_csv('/Users/yutokohata/Desktop/chores/extra_students/学生情報_20240619.csv')

# Define the center coordinate and radius
center = (35.6895, 139.6917)  # Example coordinate (latitude, longitude) for Tokyo
radius_km = 20

# Function to check if a university is within the specified radius
def is_within_radius(lat, lon, center, radius_km):
    return geodesic(center, (lat, lon)).km <= radius_km

# Filter universities within the 70km radius
uni_coords['within_radius'] = uni_coords.apply(lambda row: is_within_radius(row['lat'], row['lon'], center, radius_km), axis=1)
nearby_universities = uni_coords[uni_coords['within_radius']]['name'].tolist()

# 2025年3月以降の卒業予定者をフィルタリング
student_info['卒業予定'] = pd.to_datetime(student_info['卒業予定'], errors='coerce')
filtered_graduation_students = student_info[student_info['卒業予定'] >= '2026-03-01']

# Filter student records based on university names and region
filtered_students = filtered_graduation_students[
    student_info['学校名'].isin(nearby_universities)
]

# Concatenate 姓 and 名 columns to form a 名前 column
filtered_students['名前'] = filtered_students['姓'] + ' ' + filtered_students['名']

# Select only the required columns
filtered_students = filtered_students[['メールアドレス', '名前']]

# Output the result to a new CSV file
output_path = '/Users/yutokohata/Desktop/chores/extra_students/filtered_student.csv'
filtered_students.to_csv(output_path, index=False)

print(f"The filtered student information has been saved to {output_path}")