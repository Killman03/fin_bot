from openpyxl import Workbook

from database.requests import get_note_info, get_all_notes


# Определение функции для экспорта данных в XLSX
async def export_to_xlsx(user_id: int):
    global name
    wb = Workbook()
    COLUMN_NAMES = ["№", "Сумма", "Примичание", "Дата"]

    for table_num in [1, 2]:
        items = await get_all_notes(table_num, user_id)
        for item in items:
            count = 0
            note_info = await get_note_info(table_num, item.id)
            ws = wb.create_sheet(item.name)
            ws.append(COLUMN_NAMES)
            for note in note_info:
                if note is not None:
                    ws.column_dimensions['C'].width = 30
                    ws.column_dimensions['D'].width = 30
                    count += 1
                    ws.append([count, note.amount, note.description, note.created])
                else:
                    print("Note is None")

    # wb.remove_sheet(wb.get_sheet_by_name('Sheet'))
    name = 'documents/budget.xlsx'
    wb.save(name)