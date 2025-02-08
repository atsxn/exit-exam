from flask import Flask, jsonify, request
import json

app = Flask(__name__)

#ฟังก์ชันสำหรับโหลดข้อมูลจากไฟล์ JSON
def load_data():
    with open("driverdata.json", "r", encoding="utf-8") as f:
        return json.load(f)

#ฟังก์ชันสำหรับบันทึกข้อมูลลงไฟล์ JSON
def save_data(data):
    with open("driverdata.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#อ่านข้อมูลทั้งหมด
@app.route('/drivers', methods=['GET'])
def get_drivers():
    drivers = load_data()
    return jsonify(drivers)

#อ่านข้อมูลของไดร์เวอร์โดยใช้ license_number
@app.route('/drivers/<license_number>', methods=['GET'])
def get_driver(license_number):
    drivers = load_data()
    driver = next((d for d in drivers if d["license_number"] == license_number), None)

    if driver is None:
        return jsonify({"message": "Driver not found"}), 404
    return jsonify(driver)

#Route: เพิ่มข้อมูลไดร์เวอร์ใหม่
@app.route('/drivers', methods=['POST'])
def add_driver():
    new_driver = request.get_json()
    drivers = load_data()

    #ตรวจสอบว่ามี license_number นี้แล้วหรือไม่
    if any(d["license_number"] == new_driver["license_number"] for d in drivers):
        return jsonify({"message": "Driver already exists"}), 400

    drivers.append(new_driver)
    save_data(drivers)

    return jsonify(new_driver), 201

#Route: แก้ไขข้อมูลของไดร์เวอร์
@app.route('/drivers/<license_number>', methods=['PUT'])
def update_driver(license_number):
    updated_driver = request.get_json()
    drivers = load_data()

    driver = next((d for d in drivers if d["license_number"] == license_number), None)

    if driver is None:
        return jsonify({"message": "Driver not found"}), 404

    driver.update(updated_driver)
    save_data(drivers)

    return jsonify(driver)

#Route: ลบข้อมูลของไดร์เวอร์
@app.route('/drivers/<license_number>', methods=['DELETE'])
def delete_driver(license_number):
    drivers = load_data()

    driver = next((d for d in drivers if d["license_number"] == license_number), None)

    if driver is None:
        return jsonify({"message": "Driver not found"}), 404

    drivers.remove(driver)
    save_data(drivers)

    return jsonify({"message": "Driver deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
