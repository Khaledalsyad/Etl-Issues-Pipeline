from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


OUT = Path("output/pdf/etl_project_review_guide_ar.pdf")
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
W, H = letter
MARGIN = 54
BLUE = HexColor("#2E74B5")
INK = HexColor("#0B2545")
MUTED = HexColor("#4B5563")
PALE = HexColor("#E8EEF5")

# Arabic presentation forms: isolated, final, initial, medial.
FORMS = {
    'ا': ('\ufe8d','\ufe8e',None,None), 'أ': ('\ufe83','\ufe84',None,None), 'إ': ('\ufe87','\ufe88',None,None),
    'آ': ('\ufe81','\ufe82',None,None), 'ب': ('\ufe8f','\ufe90','\ufe91','\ufe92'), 'ت': ('\ufe95','\ufe96','\ufe97','\ufe98'),
    'ث': ('\ufe99','\ufe9a','\ufe9b','\ufe9c'), 'ج': ('\ufe9d','\ufe9e','\ufe9f','\ufea0'), 'ح': ('\ufea1','\ufea2','\ufea3','\ufea4'),
    'خ': ('\ufea5','\ufea6','\ufea7','\ufea8'), 'د': ('\ufea9','\ufeaa',None,None), 'ذ': ('\ufeab','\ufeac',None,None),
    'ر': ('\ufead','\ufeae',None,None), 'ز': ('\ufeaf','\ufeb0',None,None), 'س': ('\ufeb1','\ufeb2','\ufeb3','\ufeb4'),
    'ش': ('\ufeb5','\ufeb6','\ufeb7','\ufeb8'), 'ص': ('\ufeb9','\ufeba','\ufebb','\ufebc'), 'ض': ('\ufebd','\ufebe','\ufebf','\ufec0'),
    'ط': ('\ufec1','\ufec2','\ufec3','\ufec4'), 'ظ': ('\ufec5','\ufec6','\ufec7','\ufec8'), 'ع': ('\ufec9','\ufeca','\ufecb','\ufecc'),
    'غ': ('\ufecd','\ufece','\ufecf','\ufed0'), 'ف': ('\ufed1','\ufed2','\ufed3','\ufed4'), 'ق': ('\ufed5','\ufed6','\ufed7','\ufed8'),
    'ك': ('\ufed9','\ufeda','\ufedb','\ufedc'), 'ل': ('\ufedd','\ufede','\ufedf','\ufee0'), 'م': ('\ufee1','\ufee2','\ufee3','\ufee4'),
    'ن': ('\ufee5','\ufee6','\ufee7','\ufee8'), 'ه': ('\ufee9','\ufeea','\ufeeb','\ufeec'), 'و': ('\ufeed','\ufeee',None,None),
    'ى': ('\ufeef','\ufef0',None,None), 'ي': ('\ufef1','\ufef2','\ufef3','\ufef4'), 'ة': ('\ufe93','\ufe94',None,None),
    'ؤ': ('\ufe85','\ufe86',None,None), 'ئ': ('\ufe89','\ufe8a','\ufe8b','\ufe8c'), 'ء': ('\ufe80',None,None,None),
}
RIGHT_JOINING = set('ا��إآدذرزوؤء')


def joins_left(ch):
    return ch in FORMS and ch not in RIGHT_JOINING


def joins_right(ch):
    return ch in FORMS and ch not in RIGHT_JOINING


def shape(text):
    chars = list(text)
    out = []
    for i, ch in enumerate(chars):
        if ch not in FORMS:
            out.append(ch)
            continue
        prev = chars[i - 1] if i else ''
        nxt = chars[i + 1] if i + 1 < len(chars) else ''
        connect_prev = joins_left(prev) and joins_right(ch)
        connect_next = joins_left(ch) and joins_right(nxt)
        forms = FORMS[ch]
        index = 3 if connect_prev and connect_next else 1 if connect_prev else 2 if connect_next else 0
        out.append(forms[index] or forms[0])
    return ''.join(out)[::-1]


def wrap(text, font, size, width):
    words = text.split()
    lines, current = [], []
    for word in words:
        candidate = ' '.join(current + [word])
        if current and pdfmetrics.stringWidth(shape(candidate), font, size) > width:
            lines.append(' '.join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))
    return lines


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont('Arabic', FONT_PATH))
    c = Canvas(str(OUT), pagesize=letter)
    c.setTitle('دليل مراجعة مشاريع ETL')
    y = H - MARGIN

    def header():
        nonlocal y
        c.setFillColor(MUTED); c.setFont('Arabic', 8)
        c.drawString(MARGIN, H - 34, 'ETL PROJECT REVIEW GUIDE')
        c.setStrokeColor(HexColor('#D1D5DB')); c.line(MARGIN, H - 40, W - MARGIN, H - 40)
        y = H - 68

    def new_page():
        c.showPage(); header()

    def rtl(text, size=10.5, color=INK, leading=16, gap=4):
        nonlocal y
        lines = wrap(text, 'Arabic', size, W - 2 * MARGIN)
        if y - leading * len(lines) < MARGIN:
            new_page()
        c.setFillColor(color); c.setFont('Arabic', size)
        for line in lines:
            c.drawRightString(W - MARGIN, y, shape(line)); y -= leading
        y -= gap

    def section(title, bullets):
        nonlocal y
        if y < 130:
            new_page()
        c.setFillColor(BLUE); c.setFont('Arabic', 15)
        c.drawRightString(W - MARGIN, y, shape(title)); y -= 24
        for item in bullets:
            lines = wrap(item, 'Arabic', 10.5, W - 2 * MARGIN - 20)
            if y - 16 * len(lines) < MARGIN:
                new_page()
            c.setFillColor(BLUE); c.circle(W - MARGIN - 5, y + 3, 2, fill=1, stroke=0)
            c.setFillColor(INK); c.setFont('Arabic', 10.5)
            for line in lines:
                c.drawRightString(W - MARGIN - 16, y, shape(line)); y -= 16
            y -= 3

    header()
    c.setFillColor(INK); c.setFont('Arabic', 26)
    c.drawRightString(W - MARGIN, y, shape('دليل مراجعة مشاريع إي تي إل')); y -= 32
    c.setFillColor(MUTED); c.setFont('Arabic', 13)
    c.drawRightString(W - MARGIN, y, shape('أخطاء شائعة، أسبابها، وقائمة مراجعة قبل الإنتاج')); y -= 32
    c.setFillColor(PALE); c.roundRect(MARGIN, y - 46, W - 2 * MARGIN, 42, 7, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont('Arabic', 10.5)
    c.drawRightString(W - MARGIN - 12, y - 20, shape('خط البيانات الناجح لا ينقل البيانات فقط؛ بل يضمن صحتها واكتمالها وإمكانية إعادة تشغيله ومراجعته.'))
    y -= 66

    section('١. قبل كتابة الكود', [
        'ثبّت عقد البيانات أولًا: اسم الحقل، نوعه، مصدره، هل يقبل قيمة فارغة، ومفتاحه وعلاقاته.',
        'راجع بيانات حقيقية من المصدر. لا تفترض أن المعرف رقم؛ قد يكون نصًا لا يحمل معنى رقميًا.',
        'وحّد أسماء الحقول بين الاستعلام والتحويل والتحقق وقاعدة البيانات.',
    ])
    section('٢. الاستخراج من المصدر', [
        'اختبر التقسيم إلى صفحات ببيانات تتجاوز حجم الصفحة؛ خطأ عودة مبكرة قد يفقد معظم البيانات.',
        'راجع الصفحات للعلاقات الداخلية أيضًا، مثل التصنيفات والتعيينات والتعليقات.',
        'استخدم مهلة زمنية وإعادة محاولة تدريجية، واحترم حدود الطلبات.',
        'لا تحدد عددًا صغيرًا للعناصر دون قرار صريح وتسجيل واضح؛ فقد البيانات الصامت أخطر الأخطاء.',
    ])
    section('٣. التحويل وجودة البيانات', [
        'لا تجعل الحقل إلزاميًا إذا كان المصدر لا يضمنه. عالج القيم الفارغة والأنواع غير المتوقعة.',
        'تحقق من الأعمدة والمفاتيح والتكرار والقيم الفارغة قبل التحميل.',
        'أضف معرف التشغيل ووقت الاستخراج ووقت التحميل ومصدر السجل من أول يوم.',
        'اختبر عينات تشمل قيمًا فارغة وتكرارًا وعلاقات بلا عناصر.',
    ])
    section('٤. التحميل والمنطق التزايدي', [
        'اجعل التحميل قابلاً لإعادة التشغيل بأمان؛ لا يكرر السجلات ولا يفسد النتائج.',
        'أنشئ سجل آخر تشغيل ضمن المخطط، ولا تحدّثه إلا بعد نجاح التحميل كاملًا.',
        'حدد هل تريد لقطة حالية أم تاريخًا. الإضافة وحدها لا تزيل علاقة حُذفت من المصدر.',
        'استخدم معاملة واحدة للتحميل، وخطط للبيانات المتأخرة والأحداث ذات الوقت المتساوي.',
    ])
    section('٥. الجاهزية للإنتاج', [
        'استخدم ترحيلات للمخطط بدل تعديلات يدوية، وجرّبها على بيئة غير إنتاجية أولًا.',
        'ضع كل التبعيات في ملف موحد واختبر المشروع داخل بيئة نظيفة.',
        'أبقِ الأسرار خارج المستودع والسجلات، وأضف اختبارات ومراقبة وتنبيهات للفشل.',
    ])
    if y < 250:
        new_page()
    c.setFillColor(BLUE); c.setFont('Arabic', 15)
    c.drawRightString(W - MARGIN, y, shape('قائمة الفحص قبل النشر')); y -= 28
    checks = [
        'راجعت عينة حقيقية من المصدر وأنواع المعرفات والحقول الاختيارية.',
        'كل تقسيم إلى صفحات مغطى باختبار يتجاوز حجم الصفحة.',
        'المخطط والتحويل والاستعلامات تستخدم أسماء وأنواعًا متطابقة.',
        'التحميل آمن لإعادة التشغيل وتوجد سياسة للحذف وتحديث العلاقات.',
        'سجل آخر تشغيل موجود ولا يتحدث قبل اكتمال التحميل.',
        'التبعيات والتشغيل ينجحان في بيئة نظيفة.',
        'الأسرار خارج المستودع ولا تظهر في السجلات.',
        'توجد اختبارات ومراقبة وتنبيه للفشل.',
    ]
    for item in checks:
        if y < MARGIN + 20:
            new_page()
        c.setFillColor(PALE if int(y) % 2 else white)
        c.roundRect(MARGIN, y - 16, W - 2 * MARGIN, 22, 3, fill=1, stroke=0)
        c.setFillColor(DARK := HexColor('#1F4D78')); c.setFont('Arabic', 11)
        c.drawString(MARGIN + 10, y - 1, '□')
        c.setFillColor(INK); c.setFont('Arabic', 10.5)
        c.drawRightString(W - MARGIN - 12, y - 1, shape(item)); y -= 28
    y -= 8
    rtl('قاعدة أخيرة: اسأل دائمًا هل البيانات صحيحة، كاملة، قابلة لإعادة التشغيل، وقابلة للتفسير. إذا لم تكن الإجابة نعم على الأربعة، فالخط ليس جاهزًا بعد.', 11, INK, 17, 0)
    c.save()
    print(OUT.resolve())


if __name__ == '__main__':
    build()
