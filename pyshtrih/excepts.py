# -*- coding: utf-8 -*-


import misc
from handlers import commands as hc


class ProtocolError(IOError):

    def __str__(self):
        if self.errno is None:
            message = self.message
        else:
            # метод __str__ вернет str, если strerror является str
            # метод __str__ вернет unicode, если strerror является unicode
            message = super(ProtocolError, self).__str__()

        if isinstance(message, str):
            return message
        else:
            return message.encode(misc.LOCALE)

    def __unicode__(self):
        return str(self).decode(misc.LOCALE)


class NoConnectionError(ProtocolError):
    
    def __init__(self, *args):
        if not args:
            args = (u'Нет связи с ККМ', )
        super(NoConnectionError, self).__init__(*args)


class UnexpectedResponseError(ProtocolError):
    pass


class FDError(ProtocolError):
    pass


class Error(ProtocolError):

    codes = {
        0x00: u'Ошибок нет',
        0x01: u'Неисправен накопитель ФП 1, ФП 2 или часы',
        0x02: u'Отсутствует ФП 1',
        0x03: u'Отсутствует ФП 2',
        0x04: u'Некорректные параметры в команде обращения к ФП',
        0x05: u'Нет запрошенных данных',
        0x06: u'ФП в режиме вывода данных',
        0x07: u'Некорректные параметры в команде для данной реализации ФП',
        0x08: u'Команда не поддерживается в данной реализации ФП',
        0x09: u'Некорректная длина команды',
        0x0A: u'Формат данных не BCD',
        0x0B: u'Неисправна ячейка памяти ФП при записи итога',
        0x0C: u'Переполнение необнуляемой суммы',
        0x0D: u'Переполнение суммы итогов смен',
        0x11: u'Не введена лицензия',
        0x12: u'Заводской номер уже введен',
        0x13: u'Текущая дата меньше даты последней записи в ФП',
        0x14: u'Область сменных итогов ФП переполнена',
        0x15: u'Смена уже открыта',
        0x16: u'Смена не открыта',
        0x17: u'Номер первой смены больше номера последней смены',
        0x18: u'Дата первой смены больше даты последней смены',
        0x19: u'Нет данных в ФП',
        0x1A: u'Область перерегистраций в ФП переполнена',
        0x1B: u'Заводской номер не введен',
        0x1C: u'В заданном диапазоне есть поврежденная запись',
        0x1D: u'Повреждена последняя запись сменных итогов',
        0x1E: u'Запись фискализации (перерегистрации ККМ) в накопителе не найдена',
        0x1F: u'Отсутствует память регистров',
        0x20: u'Переполнение денежного регистра при добавлении',
        0x21: u'Вычитаемая сумма больше содержимого денежного регистра',
        0x22: u'Неверная дата',
        0x23: u'Нет записи активизации',
        0x24: u'Область активизаций переполнена',
        0x25: u'Нет активизации с запрашиваемым номером',
        0x26: u'В ФП присутствует 3 или более битые записи сменных итогов.',
        0x27: u'Признак несовпадения КС, з/н, перерегистраций или активизаций',
        0x28: u'Технологическая метка в накопителе присутствует',
        0x29: u'Технологическая метка в накопителе отсутствует, возможно накопитель пуст',
        0x2A: u'Фактическая емкость микросхемы накопителя не соответствует текущей версии ПО',
        0x2B: u'Невозможно отменить предыдущую команду',
        0x2C: u'Обнулённая касса (повторное гашение невозможно)',
        0x2D: u'Сумма чека по секции меньше суммы сторно',
        0x2E: u'В ККТ нет денег для выплаты',
        0x2F: u'Не совпадает заводской номер ККМ в оперативной памяти ФП с номером в накопителе',
        0x30: u'ККТ заблокирован, ждет ввода пароля налогового инспектора',
        0x31: u'Сигнатура емкости накопителя не соответствует текущей версии ПО',
        0x32: u'Требуется выполнение общего гашения',
        0x33: u'Некорректные параметры в команде',
        0x34: u'Нет данных',
        0x35: u'Некорректный параметр при данных настройках',
        0x36: u'Некорректные параметры в команде для данной реализации ККТ',
        0x37: u'Команда не поддерживается в данной реализации ККТ',
        0x38: u'Ошибка в ПЗУ',
        0x39: u'Внутренняя ошибка ПО ККТ',
        0x3A: u'Переполнение накопления по надбавкам в смене',
        0x3B: u'Переполнение накопления в смене',
        0x3C: u'ЭКЛЗ: неверный регистрационный номер',
        0x3D: u'Смена не открыта – операция невозможна',
        0x3E: u'Переполнение накопления по секциям в смене',
        0x3F: u'Переполнение накопления по скидкам в смене',
        0x40: u'Переполнение диапазона скидок',
        0x41: u'Переполнение диапазона оплаты наличными',
        0x42: u'Переполнение диапазона оплаты типом 2',
        0x43: u'Переполнение диапазона оплаты типом 3',
        0x44: u'Переполнение диапазона оплаты типом 4',
        0x45: u'Сумма всех типов оплаты меньше итога чека',
        0x46: u'Не хватает наличности в кассе',
        0x47: u'Переполнение накопления по налогам в смене',
        0x48: u'Переполнение итога чека',
        0x49: u'Операция невозможна в открытом чеке данного типа',
        0x4A: u'Открыт чек – операция невозможна',
        0x4B: u'Буфер чека переполнен',
        0x4C: u'Переполнение накопления по обороту налогов в смене',
        0x4D: u'Вносимая безналичной оплатой сумма больше суммы чека',
        0x4E: u'Смена превысила 24 часа',
        0x4F: u'Неверный пароль',
        0x50: u'Идет печать результатов выполнения предыдущей команды',
        0x51: u'Переполнение накоплений наличными в смене',
        0x52: u'Переполнение накоплений по типу оплаты 2 в смене',
        0x53: u'Переполнение накоплений по типу оплаты 3 в смене',
        0x54: u'Переполнение накоплений по типу оплаты 4 в смене',
        0x55: u'Чек закрыт – операция невозможна',
        0x56: u'Нет документа для повтора',
        0x57: u'ЭКЛЗ: количество закрытых смен не совпадает с ФП',
        0x58: u'Ожидание команды продолжения печати',
        0x59: u'Документ открыт другим оператором',
        0x5A: u'Скидка превышает накопления в чеке',
        0x5B: u'Переполнение диапазона надбавок',
        0x5C: u'Понижено напряжение 24В',
        0x5D: u'Таблица не определена',
        0x5E: u'Неверная операция',
        0x5F: u'Отрицательный итог чека',
        0x60: u'Переполнение при умножении',
        0x61: u'Переполнение диапазона цены',
        0x62: u'Переполнение диапазона количества',
        0x63: u'Переполнение диапазона отдела',
        0x64: u'ФП отсутствует',
        0x65: u'Не хватает денег в секции',
        0x66: u'Переполнение денег в секции',
        0x67: u'Ошибка связи с ФП',
        0x68: u'Не хватает денег по обороту налогов',
        0x69: u'Переполнение денег по обороту налогов',
        0x6A: u'Ошибка питания в момент ответа по I2C',
        0x6B: u'Нет чековой ленты',
        0x6C: u'Нет контрольной ленты',
        0x6D: u'Не хватает денег по налогу',
        0x6E: u'Переполнение денег по налогу',
        0x6F: u'Переполнение по выплате в смене',
        0x70: u'Переполнение ФП',
        0x71: u'Ошибка отрезчика',
        0x72: u'Команда не поддерживается в данном подрежиме',
        0x73: u'Команда не поддерживается в данном режиме',
        0x74: u'Ошибка ОЗУ',
        0x75: u'Ошибка питания',
        0x76: u'Ошибка принтера: нет импульсов с тахогенератора',
        0x77: u'Ошибка принтера: нет сигнала с датчиков',
        0x78: u'Замена ПО',
        0x79: u'Замена ФП',
        0x7A: u'Поле не редактируется',
        0x7B: u'Ошибка оборудования',
        0x7C: u'Не совпадает дата',
        0x7D: u'Неверный формат даты',
        0x7E: u'Неверное значение в поле длины',
        0x7F: u'Переполнение диапазона итога чека',
        0x80: u'Ошибка связи с ФП (превышен таймаут I2C с контроллером)',
        0x81: u'Ошибка связи с ФП (контроллер отсутствует!? (получен NAK по I2C) '
              u'или принят неполный кадр от контроллера UART)',
        0x82: u'Ошибка связи с ФП (неверный формат данных в кадре I2C)',
        0x83: u'Ошибка связи с ФП (неверная контрольная сумма передаваемого кадра по I2C)',
        0x84: u'Переполнение наличности',
        0x85: u'Переполнение по продажам в смене',
        0x86: u'Переполнение по покупкам в смене',
        0x87: u'Переполнение по возвратам продаж в смене',
        0x88: u'Переполнение по возвратам покупок в смене',
        0x89: u'Переполнение по внесению в смене',
        0x8A: u'Переполнение по надбавкам в чеке',
        0x8B: u'Переполнение по скидкам в чеке',
        0x8C: u'Отрицательный итог надбавки в чеке',
        0x8D: u'Отрицательный итог скидки в чеке',
        0x8E: u'Нулевой итог чека',
        0x8F: u'Касса не фискализирована',
        0x90: u'Поле превышает размер, установленный в настройках',
        0x91: u'Выход за границу поля печати при данных настройках шрифта',
        0x92: u'Наложение полей',
        0x93: u'Восстановление ОЗУ прошло успешно',
        0x94: u'Исчерпан лимит операций в чеке',
        0x95: u'Неизвестная ошибка ЭКЛЗ',
        0x96: u'Выполните суточный отчет с гашением',
        0x9B: u'Некорректное действие',
        0x9C: u'Товар не найден по коду в базе товаров',
        0x9D: u'Неверные данные в записе о товаре в базе товаров',
        0x9E: u'Неверный размер файла базы или регистров товаров',
        0xA0: u'Ошибка связи с ЭКЛЗ',
        0xA1: u'ЭКЛЗ отсутствует',
        0xA2: u'ЭКЛЗ: Некорректный формат или параметр команды',
        0xA3: u'Некорректное состояние ЭКЛЗ',
        0xA4: u'Авария ЭКЛЗ',
        0xA5: u'Авария КС в составе ЭКЛЗ',
        0xA6: u'Исчерпан временной ресурс ЭКЛЗ',
        0xA7: u'ЭКЛЗ переполнена',
        0xA8: u'ЭКЛЗ: Неверные дата и время',
        0xA9: u'ЭКЛЗ: Нет запрошенных данных',
        0xAA: u'Переполнение ЭКЛЗ (отрицательный итог документа)',
        0xAF: u'Некорректные значения принятых данных от ЭКЛЗ',
        0xB0: u'ЭКЛЗ: Переполнение в параметре количество',
        0xB1: u'ЭКЛЗ: Переполнение в параметре сумма',
        0xB2: u'ЭКЛЗ: Уже активизирована',
        0xB4: u'Найденная запись фискализации (регистрации ККМ) повреждена',
        0xB5: u'Запись заводского номера ККМ повреждена',
        0xB6: u'Найденная запись активизации ЭКЛЗ повреждена',
        0xB7: u'Записи сменных итогов в накопителе не найдены',
        0xB8: u'Последняя запись сменных итогов не записана',
        0xB9: u'Сигнатура версии структуры данных в накопителе не совпадает с текущей версией ПО',
        0xBA: u'Структура накопителя повреждена',
        0xBB: u'Текущая дата+время меньше даты+времени последней записи активизации ЭКЛЗ',
        0xBC: u'Текущая дата+время меньше даты+времени последней записи фискализации (перерегистрации ККМ)',
        0xBD: u'Текущая дата меньше даты последней записи сменного итога',
        0xBE: u'Команда не поддерживается в текущем состоянии',
        0xBF: u'Инициализация накопителя невозможна',
        0xC0: u'Контроль даты и времени (подтвердите дату и время)',
        0xC1: u'ЭКЛЗ: суточный отчёт с гашением прервать нельзя',
        0xC2: u'Превышение напряжения в блоке питания',
        0xC3: u'Несовпадение итогов чека и ЭКЛЗ',
        0xC4: u'Несовпадение номеров смен',
        0xC5: u'Буфер подкладного документа пуст',
        0xC6: u'Подкладной документ отсутствует',
        0xC7: u'Поле не редактируется в данном режиме',
        0xC8: u'Отсутствуют импульсы от таходатчика',
        0xC9: u'Перегрев печатающей головки',
        0xCA: u'Температура вне условий эксплуатации',
        0xCB: u'Неверный подытог чека',
        0xCC: u'Смена в ЭКЛЗ уже закрыта',
        0xCD: u'Обратитесь в ЦТО: тест целостности архива ЭКЛЗ не прошел, '
              u'код ошибки ЭКЛЗ можно запросить командой 10H',
        0xCE: u'Лимит минимального свободного объема ОЗУ или ПЗУ на ККМ исчерпан',
        0xCF: u'Неверная дата (Часы сброшены? Установите дату!)',
        0xD0: u'Отчет по контрольной ленте не распечатан!',
        0xD1: u'Нет данных в буфере',
        0xD5: u'Критическая ошибка при загрузке ERRxx',
        0xE0: u'Ошибка связи с купюроприемником',
        0xE1: u'Купюроприемник занят',
        0xE2: u'Итог чека не соответствует итогу купюроприемника',
        0xE3: u'Ошибка купюроприемника',
        0xE4: u'Итог купюроприемника не нулевой'
    }

    fs_codes = {
        0x00: u'Успешное выполнение команды',
        0x01: u'Неизвестная команда, неверный формат посылки или неизвестные параметры',
        0x02: u'Неверное состояние ФН',
        0x03: u'Ошибка ФН',
        0x04: u'Ошибка КС',
        0x05: u'Закончен срок эксплуатации ФН',
        0x06: u'Архив ФН переполнен',
        0x07: u'Неверные дата и/или время',
        0x08: u'Нет запрошенных данных',
        0x09: u'Некорректное значение параметров команды',
        0x10: u'Превышение размеров TLV данных',
        0x11: u'Нет транспортного соединения',
        0x12: u'Исчерпан ресурс КС (криптографического сопроцессора)',
        0x14: u'Исчерпан ресурс хранения',
        0x15: u'Исчерпан ресурс Ожидания передачи сообщения',
        0x16: u'Продолжительность смены более 24 часов',
        0x17: u'Неверная разница во времени между 2 операцими',
        0x20: u'Сообщение от ОФД не может быть принято'
    }

    def __init__(self, cmd=None, code=None, message=None, fs=False):
        self.cmd = cmd or 0x00
        self.cmd_name = hc.COMMANDS.get(cmd, u'Неизвестная команда')
        self.fs = fs
        self.code = code or 0xFF

        if self.fs and self.code in self.fs_codes:
            self.code_desc = self.fs_codes[self.code]
        else:
            self.code_desc = self.codes.get(self.code, u'Неизвестная ошибка')

        if message:
            self.template = u'{message}'
            self.message = message if isinstance(message, unicode) else message.decode(misc.LOCALE)
        else:
            self.template = u'0x{cmd:02X} ({cmd_name}) - {message} (0x{code:02X})'
            self.message = self.code_desc

    def __str__(self):
        return unicode(self).encode(misc.LOCALE)

    def __unicode__(self):
        return self.template.format(**self.__dict__)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self)


class CheckError(Error):

    def __init__(self, exc):
        if isinstance(exc, Error):
            super(CheckError, self).__init__(cmd=exc.cmd, code=exc.code, fs=exc.fs)
        elif isinstance(exc, ProtocolError):
            super(CheckError, self).__init__(message=unicode(exc))
        else:
            raise ValueError(
                'Ожидался экземпляр класса {} или его подклассов, получен {}.'.format(
                    ProtocolError.__name__,
                    type(exc).__name__
                )
            )


class OpenCheckError(CheckError):
    pass


class ItemSaleError(CheckError):
    pass


class CloseCheckError(CheckError):
    pass
