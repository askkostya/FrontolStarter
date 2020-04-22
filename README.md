<h1>Скрипт запуска Frontol</h1>
<h2>Введение</h2>
<blockquote>
<p>Иногда при запуске Фронтол необходимо дождаться пока запустятся критичные службы для работы программы VPN, УТМ, прочее</p>
<p>Скрипт делает задержку перед запуском программы, проверяет запущены ли требуемые службы, также проверяет доступность страницы УТМ</p>
<p>Если службы не запущены предпринимается попытка(и) запуска</p>

<p>Основное назначение - дождаться полного запуска Универсального транспортного модуля и готовности страницы, иначе при запуске программы выйдет сообщение о недоступости УТМ</p>
</blockquote>
<h2>Настройки программы</h2>
<blockquote>
<p>Все настройки расположены в текстовом файле initfrstarter.ini</p>
</blockquote>
<blockquote><span style="color: #0000ff;"><strong>FrontolPath = C:\Program Files (x86)\ATOL\Frontol6\BIN\Frontol.exe</strong><br /></span>Путь к файлу запуска программы</blockquote>
<blockquote><strong><span style="color: #0000ff;">utmURL = <a href="http://localhost:8080/info/version">http://localhost:8080/info/version</a><br /></span></strong>HTTP адрес страницы УТМ. Данный параметр не будет использоваться если значение waitUTMPage=0 Оставьте значение по умолчанию если не требуется проверять состояние УТМ</blockquote>
<blockquote><span style="color: #0000ff;"><strong>servicesNeedStart = Transport, Transport-Updater</strong><br /></span>Список сервисов через запятую состояние которых необходимо проверить</blockquote>
<blockquote><span style="color: #0000ff;"><strong>serviceRetryCount = 5<br /></strong></span>Количество попыток запуска служб</blockquote>
<blockquote><span style="color: #0000ff;"><strong>waitUTMPage=1<br /></strong></span>Ожидать готовность страницы УТМ. Если готовность УТМ проверять не требуется, необходимо данный параметр установить в 0</blockquote>
<blockquote><span style="color: #0000ff;"><strong>utmwwwRetryCount = 10<br /></strong></span>Количество попыток проверки доступности страницы УТМ</blockquote>
<blockquote>ВНИМАНИЕ. Для работы с сервисами пользователю от которого запускается скрипт требуются административные права svcadmin позволяет задать права доступа на запуск определенных сервисов</blockquote>