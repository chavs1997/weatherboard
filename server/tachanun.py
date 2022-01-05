# encoding=utf-8


import datetime
import jinja2
import os
from flask import Flask
from jewish import JewishDate

app = Flask(__name__)
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# TODO: Print Jewish date in Hebrew

MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6

@app.route('/')
def tachanun_today():
    today = datetime.date.today()
    jewish_today = JewishDate.from_date(today)
    year, month, day = (jewish_today.year, jewish_today.month, jewish_today.day)
    dow = today.weekday()
    if month == JewishDate.NISAN:
        tachanun = _no(
                'All of Nissan',
                'כל חודש ניסן')
    elif month == JewishDate.TISHREI and day in (1, 2):
        tachanun = _no( "Rosh Hashannah", 'ראש השנה')
    elif month == JewishDate.TISHREI and day == 9:
        tachanun = _no('Erev Yom Kipur', 'ערב יום כיפור')
    elif month == JewishDate.TISHREI and day >= 11:
        tachanun = _no(
                'After Yom Kipur until the end of Tishrei',
                'ממוצאי יום כיפור עד סוף חודש תשרי')
    elif ((month == JewishDate.KISLEV and day >= 25)
          or (month == JewishDate.TEVET and day <= 25 + 7 - _days_in_kislev(year))):
        tachanun = _no('Channukah', 'חנוכה שמח')
    elif month == JewishDate.SHEVAT and day == 15:
        tachanun = _no("Tu B'Shvat", 'ט"ו בשבט')
    elif month == JewishDate.ADAR_I and day in (14, 15):
        tachanun = _no('Purim Katan', 'פורים קטן')
    elif month == JewishDate.ADAR_II and day == 14:
        tachanun = _no('Purim', 'פורים')
    elif month == JewishDate.ADAR_II and day == 15:
        tachanun = _no('Shushan Purim', 'שושן פורים')
    elif month == JewishDate.ADAR_II and day == 16 and dow == SUN:
        tachanun = _no('Purim Meshulash', 'פורים משולש')
    elif month == JewishDate.IYAR and (day, dow) in ((3, THU), (4, THU), (5, WED), (6, TUE)):
        # See https://en.wikipedia.org/wiki/Independence_Day_(Israel)#Timing
        # It could be on a Monday until 2003 / 5763
        tachanun = _no("Yom Ha'atzmaut", 'יום העצמאות')
    elif month == JewishDate.IYAR and day == 14:
        tachanun = _no('Pesach Sheni', 'פסח שני')
    elif month == JewishDate.IYAR and day == 18:
        tachanun = _no("Lag B'Omer", 'ל"ג בעומר')
    elif month == JewishDate.IYAR and day == 28:
        tachanun = _no('Yom Yerushalayim', 'יום שחרור ירושלים')
    elif month == JewishDate.SIVAN and day <= 12:
        tachanun = _no('First 12 days of Sivan', 'מר"ח עד י"ב סיוון')
    elif month == JewishDate.AV and day == 9:
        tachanun = _no("Tisha B'Av", 'תשעה באב')
    elif month == JewishDate.AV and day == 15:
        tachanun = _no("Tu B'Av", 'ט"ו באב')
    elif month == JewishDate.ELUL and day == 29:
        tachanun = _no('Erev Rosh Hashannah', 'ערב ראש השנה')
    elif day in (1, 30):
        tachanun = _no( 'Rosh Chodesh', 'ראש חודש')
    elif dow == SAT:
        tachanun = _no('Shabbat shalom!', 'שבת שלום!')
    else:
        tachanun = dict(
                tachanun_en = 'Yes',
                tachanun_he = 'כן',
                reason_en = '',
                reason_he = '')

    template = JINJA_ENVIRONMENT.get_template('index.html')
    date_en = today.strftime('%A ') + str(jewish_today)
    month_he = {
        JewishDate.TISHREI: 'תשרי',
        JewishDate.CHESHVAN: 'חשון',
        JewishDate.KISLEV: 'כסלו',
        JewishDate.TEVET: 'טבת',
        JewishDate.SHEVAT: 'שבט',
        JewishDate.ADAR_I: 'אדר א\'',
        JewishDate.ADAR_II: 'אדר ב\'' if jewish_today.isLeapYear else 'אדר',
        JewishDate.NISAN: 'ניסן',
        JewishDate.IYAR: 'אייר',
        JewishDate.SIVAN: 'סיוון',
        JewishDate.TAMUZ: 'תמוז',
        JewishDate.AV: 'אב',
        JewishDate.ELUL: 'אלול',
    }[month]
    dow_he = 'יום ' + {
        SUN: "א'",
        MON: "ב'",
        TUE: "ג'",
        WED: "ד'",
        THU: "ה'",
        FRI: "ו'",
        SAT: 'שבת',
    }[dow]

    date_he = '%s %s %s %s' % (dow_he, day, month_he, year)
    return template.render(date_en=date_en, date_he=date_he, **tachanun)

def _no(en, he):
    return dict(tachanun_en='No', tachanun_he='לא', reason_en=en, reason_he=he)

def _days_in_year(year):
    return JewishDate(year + 1, JewishDate.TISHREI, 1).to_sdn() - JewishDate(year, JewishDate.TISHREI, 1).to_sdn()

def _days_in_kislev(year):
    return JewishDate(year, JewishDate.TEVET, 1).to_sdn() - JewishDate(year, JewishDate.KISLEV, 1).to_sdn()
