import pandas as pd
from datetime import datetime
import os
import xlsxwriter
from RPA.Assistant import Assistant  # นำเข้า Assistant จาก RPA.Assistant
from RPA.Excel.Files import Files

def Get_File_name(path_file):
    file_path = path_file
    file_name = os.path.basename(file_path)

    return file_name

def Select_File():
    assistant = Assistant()  # สร้างอ็อบเจ็กต์ของ Assistant

    assistant = Assistant()
    assistant.add_heading("Please select your excel.", size="large")
    assistant.open_row()

    assistant.open_column()
    assistant.add_file_input(name="select_file",file_type="xlsx",source="DATA")
    assistant.close_column()

    assistant.open_column()
    assistant.add_loading_spinner(name="loadingspiner")
    assistant.close_column()
    assistant.close_row()

    assistant.open_column()
    assistant.add_submit_buttons(buttons="Submit", default="Submit")
    result = assistant.run_dialog(height="250",title="Select File",location="Center")

    for path in result.select_file:
        path_file = path

    print("Selected file: ", path_file)

    file_path = path_file
    file_name = os.path.basename(file_path)

    print("file_name: ", file_name)

    return file_path

file_path = Select_File()
file_name = Get_File_name(file_path)

# โหลดข้อมูลจาก sheet ทั้งหมดในไฟล์ Excel
file_name = file_name  # แทนชื่อไฟล์ Excel ที่ต้องการอ่าน
excel_file = pd.ExcelFile(file_path)

sheet_names = excel_file.sheet_names
jtl_sheets = [sheet for sheet in sheet_names if '_jtl' in sheet]

# สร้างโฟลเดอร์ result หากยังไม่มี
folder_path = 'result'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# รูปแบบชื่อไฟล์ใหม่ตามที่ต้องการ (ชื่อเดิม_ddMmyyy_HHmm.xlsx)
timestamp = datetime.now().strftime("%d%m%Y_%H%M")
new_file_name = f"{file_name[:-5]}_{timestamp}.xlsx"  # นำชื่อไฟล์เดิมมาต่อกับ timestamp
new_file_path = os.path.join(folder_path, new_file_name)  # รวม path ของไฟล์ใหม่
print("new_file_path:", new_file_path)
# สร้าง ExcelWriter สำหรับการบันทึกไฟล์ Excel ใหม่
excel_writer = pd.ExcelWriter(new_file_path, engine='xlsxwriter')

# สร้าง workbook object จาก ExcelWriter
workbook = excel_writer.book

# สร้าง sheet โดยใช้ ExcelWriter
for sheet in jtl_sheets:
    workbook.add_worksheet(sheet)

for sheet in jtl_sheets:
    
    # สร้าง Style object สำหรับการจัดรูปแบบเซลล์ใน Excel
    red_background_format = excel_writer.book.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    center_format = excel_writer.book.add_format({'align': 'center'})
    
    df = pd.read_excel(file_path, sheet_name=sheet)

    
    # โค้ดที่ใช้เงื่อนไขในการจัดรูปแบบแบบเงื่อนไขใน Excel
    excel_writer.sheets[sheet].conditional_format('G2:G1000', {'type': 'cell', 'criteria': '>', 'value': 1, 'format': red_background_format})
    excel_writer.sheets[sheet].conditional_format('D2:D1000', {'type': 'cell', 'criteria': '>', 'value': 0.1, 'format': red_background_format})

    print("กำลังบันทึก sheet:", sheet)
    df = df[['Label','# Samples', 'Average','Error %', 'Min', 'Max', '95% Line', 'Throughput']]
    
    # ตรวจสอบและแสดงคอลัมน์ที่ต้องการและทำการคูณด้วย 1000 ยกเว้น 'Throughput'
    columns_to_multiply = ['Average', 'Min', 'Max', '95% Line']
    for col in columns_to_multiply:
        if col in df.columns:
            df[col] = df[col] / 1000 if col != 'Throughput' else df[col]
            df[col] = df[col].round(2)  # แปลงเป็นทศนิยม 2 ตำแหน่ง
            #df[col] = df[col].apply(lambda x: f"{x:.2f}")

    if 'Error %' in df.columns:
        # ทำการแปลงค่าในคอลัมน์ 'Error %' กลับเป็นสตริงที่แสดงเป็นเปอร์เซ็นต์
        df['Error %'] = df['Error %'].apply(lambda x: f"{x:.2%}" if pd.notnull(x) else x)
    
    # แสดง 'Throughput' เป็นทศนิยม 2 ตำแหน่ง
    if 'Throughput' in df.columns:
        df['Throughput'] = df['Throughput'].round(2)
    
    # กำหนดการจัด format สำหรับเซลล์ที่มีค่า '95% Line' มากกว่า 3000
    if sheet in excel_writer.sheets:
        
        # โค้ดที่ใช้ในการจัด format ของ cell ใน Excel
        for col_num, col_name in enumerate(df.columns):
            if col_name in ['# Samples', 'Average','Error %', 'Min', 'Max', '95% Line', 'Throughput']:
                excel_writer.sheets[sheet].set_column(col_num, col_num, None, center_format)
                
        # โค้ดที่ใช้ในการบันทึก sheet ในไฟล์ Excel
        df.to_excel(excel_writer, sheet_name=sheet, index=False)
    else:
        print(f"ไม่พบ '{sheet}' ในไฟล์ Excel")

# บันทึกไฟล์ Excel ใหม่ในโฟลเดอร์ result
excel_writer._save()
#print(f"บันทึกไฟล์ {new_file_name} ในโฟลเดอร์ {folder_path} สำเร็จ

