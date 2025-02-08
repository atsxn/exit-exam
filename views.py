import streamlit as st
import json

#ฟังก์ชันสำหรับโหลดข้อมูลจากไฟล์ JSON
def load_data():
    with open("driverdata.json", "r", encoding="utf-8") as f:
        return json.load(f)

#สไตล์ของแอปพลิเคชัน
st.set_page_config(page_title="Driver Dashboard", layout="centered")

#ส่วนหัวของแอปพลิเคชัน
st.title("Driver Dashboard")

#ฟีเจอร์การนับจำนวนของแต่ละประเภทผู้ขับขี่
drivers = load_data()

#สร้างตัวนับจำนวนประเภทผู้ขับขี่
driver_types = ["บุคคลทั่วไป", "มือใหม่", "คนขับรถสาธารณะ"]
driver_counts = {driver_type: sum(1 for d in drivers if d['driver_type'] == driver_type) for driver_type in driver_types}

#แสดงผลการนับจำนวน
st.header("จำนวนผู้ขับขี่แต่ละประเภท")
for driver_type, count in driver_counts.items():
    st.subheader(f"{driver_type}: {count} คน")

#ฟีเจอร์กรองข้อมูลผู้ขับขี่
driver_type_filter = st.selectbox("กรุณาเลือกประเภทผู้ขับขี่พื่อแสดงข้อมูล:", driver_types)
filtered_drivers = [d for d in drivers if d['driver_type'] == driver_type_filter]

#กรองตามหมายเลขใบขับขี่
license_number_filter = st.text_input("กรอกหมายเลขใบขับขี่เพื่อค้นหา (หากต้องการกรอง):")
if license_number_filter:
    filtered_drivers = [d for d in filtered_drivers if d['license_number'] == license_number_filter]

#แสดงข้อมูลของผู้ขับขี่ตามที่กรอง
st.header(f"ข้อมูลผู้ขับขี่ประเภท {driver_type_filter}")
if filtered_drivers:
    for driver in filtered_drivers:
        st.write(f"**ใบขับขี่:** {driver['license_number']}")
        st.write(f"**วันเกิด:** {driver['birth_date']}")
        st.write(f"**สถานะใบขับขี่:** {driver['license_status']}")
        st.write("---")
else:
    st.write("ไม่มีข้อมูลสำหรับประเภทนี้หรือหมายเลขใบขับขี่ที่กรอกไม่ตรงกับข้อมูล")