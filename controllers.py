from datetime import datetime
import random
from models import DriverModel
import streamlit as st


class DriverController:
    @staticmethod
    def validate_license(license_no):
        return license_no.isdigit() and len(license_no) == 9 and license_no[0] != "0"

    @staticmethod
    def get_driver_info(license_no):
        driver = DriverModel.find_driver(license_no)
        if driver:
            DriverController.update_status(driver)
        return driver

    @staticmethod
    def update_status(driver):
        birthdate = datetime.strptime(driver["birthdate"], "%d/%m/%Y")
        age = (datetime.today() - birthdate).days // 365

        if driver["type"] == "บุคคลทั่วไป":
            if age > 70:
                driver["status"] = "หมดอายุ"
            elif age < 16:
                driver["status"] = "ถูกระงับ"
                st.error("อายุต่ำกว่า 16 ปี: สถานะถูกระงับ")
            else:
                #มีปุ่มสอบทดสอบสมรรถนะ
                if st.button(f"ทดสอบสมรรถนะ {driver['name']}"):
                        st.success(f"สิ้นสุดการทดสอบสมรรถนะของ {driver['name']}")

        elif driver["type"] == "มือใหม่":
            if age > 50:
                driver["status"] = "หมดอายุ"
            elif age < 16:
                driver["status"] = "ถูกระงับ"
                st.error("อายุต่ำกว่า 16 ปี: สถานะถูกระงับ")
            else:
                #มีปุ่มสอบข้อเขียนและสอบปฏิบัติ
                if st.button(f"สอบข้อเขียน {driver['name']}"):
                    st.success(f"สิ้นสุดการสอบข้อเขียนของ {driver['name']}")
                if st.button(f"สอบปฏิบัติ {driver['name']}"):
                    st.success(f"สิ้นสุดการสอบปฏิบัติของ {driver['name']}")

        elif driver["type"] == "คนขับรถสาธารณะ":
            if age > 60:
                driver["status"] = "หมดอายุ"
            elif age < 20:
                driver["status"] = "ถูกระงับ"
                st.error("อายุต่ำกว่า 20 ปี: สถานะถูกระงับ")
            else:
                #เลขจำนวนการร้องเรียน(สุ่ม)
                complaints_count = random.randint(0, 10)
                st.write(f"จำนวนการร้องเรียน: {complaints_count}")
        
                if complaints_count > 5:
                    status = 'ถูกระงับชั่วคราว'
                    if st.button(f"อบรม {driver['name']}"):
                        st.success(f"สิ้นสุดการอบรมของ {driver['name']}")
                    if st.button(f"ทดสอบสมรรถนะ {driver['name']}"):
                        st.success(f"สิ้นสุดการทดสอบสมรรถนะของ {driver['name']}")
                else:
                    if st.button(f"ทดสอบสมรรถนะ {driver['name']}"):
                        st.success(f"สิ้นสุดการทดสอบสมรรถนะของ {driver['name']}")

        DriverModel.save_data(DriverModel.load_data())  #บันทึกการเปลี่ยนแปลง
