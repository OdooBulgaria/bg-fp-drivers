# -*- coding: utf-8 -*-


from misc import mslice, default, decode, handle_date, handle_time, handle_version, handle_fp_flags, handle_inn, \
    handle_fr_flags, FuncChain, UNCAST_SIZE, FRMode, FRSubMode


COMMANDS = {
    0x10: u'Короткий запрос состояния ФР',
    0x11: u'Запрос состояния ФР',
    0x13: u'Гудок',
    # 0x15: u'Чтение параметров обмена',
    0x17: u'Печать строки',
    0x19: u'Тестовый прогон',
    # 0x1B: u'Запрос операционного регистра',
    # 0x1E: u'Запись таблицы',
    # 0x1F: u'Чтение таблицы',
    0x21: u'Программирование времени',
    # 0x22: u'Программирование даты',
    # 0x23: u'Подтверждение программирования даты',
    0x25: u'Отрезка чека',
    0x28: u'Открыть денежный ящик',
    0x29: u'Протяжка',
    0x2B: u'Прерывание тестового прогона',
    # 0x2D: u'Запрос структуры таблицы',
    # 0x2E: u'Запрос структуры поля',
    0x40: u'Суточный отчет без гашения',
    0x41: u'Суточный отчет с гашением',
    0x50: u'Внесение',
    0x51: u'Выплата',
    # 0x80: u'Продажа',
    # 0x82: u'Возврат продажи',
    # 0x85: u'Закрытие чека',
    # 0x86: u'Скидка',
    # 0x87: u'Надбавка',
    # 0x88: u'Аннулирование чека',
    0x8C: u'Повтор документа',
    # 0x8D: u'Открыть чек',
    0xB0: u'Продолжение печати',
    # 0xC2: u'Печать штрих-кода',
    0xE0: u'Открыть смену',
    0xFC: u'Получить тип устройства'
}

ERROR_CODE_STR = u'Код ошибки'
ERROR_CODE_STRUCT = (slice(0, 1), default, ERROR_CODE_STR)
OPERATOR_INDEX_NUMBER_STRUCT = (slice(1, 2), default, u'Порядковый номер оператора')

HANDLERS = {
    0x10: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT,
        (slice(2, 4), FuncChain(handle_fr_flags, UNCAST_SIZE['2']), u'Флаги ФР'),
        (slice(4, 5), FuncChain(FRMode, UNCAST_SIZE['1']), u'Режим ФР'),
        (slice(5, 6), FuncChain(FRSubMode, UNCAST_SIZE['1']), u'Подрежим ФР'),
        (mslice(slice(11, 12), slice(6, 7)), UNCAST_SIZE['2'], u'Количество операций в чеке'),
        (slice(7, 8), default, u'Напряжение резервной батареи'),
        (slice(8, 9), default, u'Напряжение источника питания'),
        (slice(9, 10), default, u'Код ошибки ФП'),
        (slice(10, 11), default, u'Код ошибки ЭКЛЗ'),
        (slice(12, 15), None, u'Зарезервировано')
    ),
    0x11: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT,
        (slice(2, 4), FuncChain(handle_version, UNCAST_SIZE['11']), u'Версия ПО ФР'),
        (slice(4, 6), UNCAST_SIZE['2'], u'Сборка ПО ФР'),
        (slice(6, 9), FuncChain(handle_date, UNCAST_SIZE['111']), u'Дата ПО ФР'),
        (slice(9, 10), default, u'Номер в зале'),
        (slice(10, 12), UNCAST_SIZE['2'], u'Сквозной номер текущего документа'),
        (slice(12, 14), FuncChain(handle_fr_flags, UNCAST_SIZE['2']), u'Флаги ФР'),
        (slice(14, 15), FuncChain(FRMode, UNCAST_SIZE['1']), u'Режим ФР'),
        (slice(15, 16), FuncChain(FRSubMode, UNCAST_SIZE['1']), u'Подрежим ФР'),
        (slice(16, 17), default, u'Порт ФР'),
        (slice(17, 19), FuncChain(handle_version, UNCAST_SIZE['11']), u'Версия ПО ФП'),
        (slice(19, 21), UNCAST_SIZE['2'], u'Сборка ПО ФП'),
        (slice(21, 24), FuncChain(handle_date, UNCAST_SIZE['111']), u'Дата ПО ФП'),
        (slice(24, 27), FuncChain(handle_date, UNCAST_SIZE['111']), u'Дата'),
        (slice(27, 30), FuncChain(handle_time, UNCAST_SIZE['111']), u'Время'),
        (slice(30, 31), FuncChain(handle_fp_flags, UNCAST_SIZE['1']), u'Флаги ФП'),
        (slice(31, 35), UNCAST_SIZE['4'], u'Заводской номер'),
        (slice(35, 37), UNCAST_SIZE['2'], u'Номер последней закрытой смены'),
        (slice(37, 39), UNCAST_SIZE['2'], u'Количество свободных записей в ФП'),
        (slice(39, 40), default, u'Количество перерегистраций (фискализаций)'),
        (slice(40, 41), default, u'Количество оставшихся перерегистраций (фискализаций)'),
        (slice(41, 47), handle_inn, u'ИНН')
    ),
    0x13: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT,
    ),
    # TODO: написать обработчики
    0x15: (
        ERROR_CODE_STRUCT,
        (slice(1, 2), default, u'Код скорости обмена'),
        (slice(2, 3), default, u'Тайм аут приема байта')
    ),
    0x17: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0x19: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0x21: (
        ERROR_CODE_STRUCT,
    ),
    # TODO: дописать
    0x1F: (
        (slice(0, None), repr, u'Значение'),
    ),
    0x25: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0x28: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0x2B: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0x40: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0x41: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0x50: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT,
        (slice(2, None), UNCAST_SIZE['2'], u'Сквозной номер документа')
    ),
    0x51: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT,
        (slice(2, None), UNCAST_SIZE['2'], u'Сквозной номер документа')
    ),
    0x8C: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0xB0: (
        ERROR_CODE_STRUCT,
        OPERATOR_INDEX_NUMBER_STRUCT
    ),
    0xE0: (
        OPERATOR_INDEX_NUMBER_STRUCT,
    ),
    0xFC: (
        ERROR_CODE_STRUCT,
        (slice(1, 2), default, u'Тип устройства'),
        (slice(2, 3), default, u'Подтип устройства'),
        (slice(3, 4), default, u'Версия протокола для данного устройства'),
        (slice(4, 5), default, u'Подверсия протокола для данного устройства'),
        (slice(5, 6), default, u'Модель устройства'),
        (slice(6, 7), default, u'Язык устройства'),
        (slice(7, None), decode, u'Название устройства')
    )
}
