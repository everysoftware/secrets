from aiogram.filters.callback_data import CallbackData


class ShowRecordData(CallbackData, prefix='show_record'):
    record_id: int
    record_name: str
