by Tamio@2020.07.07
###環境設定(Windows & Mac)

1.   Windows到這裡下載/安裝MySQL Installer  >>  <https://dev.mysql.com/downloads/installer/>，可以不用註冊oracle會員，選擇下面的「**No thanks, just start my download.**」就好了。
2.   MacOS的話則到這裡來 >>  <https://dev.mysql.com/downloads/file/?id=495298>。
3.   有的教學會說下載MySQL Workbench就好，但我這樣做了之後發現一直連結不到MySQL Server(我的電腦環境是win10，顯示錯誤訊息【Can't connect to MySQL server on 'localhost' (10061)】)，所以我選擇下載並安裝MySQL Installer，然後安裝型態記得要選FULL!
4.   安全性是選擇「use legacy auth method」，root的密碼跟新建立的user帳號/密碼一定要抄下來，一定要!!!
5.   安裝完後，開啟MySQL Workbench就可以看到建立連線了，可喜可賀。  
<br>
    <h4>開始摸索</h4>
    1.  在MySQL中, schema就等於資料庫(database)，所以create schema == create database。
    2.  先來開啟一個django project(我使用WSL + VS Code + Python 3.7x) >> Quikok，記得加進Git的控管唷XD
    3. 來建立一個database讓Quikok連過來試試看吧，打開workbench後，在左側找到Schemas，右鍵點選Create Schema...，名稱我設「quikok_db」，其他的都default就好。
    4. 然後什麼都不用動，也不用建立Table(我們會透過migrate機制實現)，現在開始著手Django的部份。
    5. 修改 settings.py 設定，根據上面的資訊，我的設定如下:</br>
    <img src="https://lh4.googleusercontent.com/clhpWO5GLuPm9FRMXP0kHRec2oWa2qPiH83I0WhPI4EwXYhtuxu_6NEsb92Ec3d1mXR7ccIINw8hQOsjtp3C5mbB7hjP5z-SAHb_8tw0Ki5wajKV4C25o_-nftRH5Jn26QRQI497">  
    6. python manage.py runserver看看有沒有問題，>> 有問題，它問我【Did you install mysqlclient?】
安裝這個 >> pip install pymysql，然後到setting.py同資料夾的\_\_init\_\_.py加上下面這樣儲存後執行:<br>
    import pymysql<br>
    pymysql.install_as_MySQLdb()
    7. 又有問題....顯示【mysqlclient 1.3.13 or newer is required; you have 0.9.3.】
到錯誤倒數第三行 >> 「File "/home/tamio/anaconda3/envs/quikok/lib/python3.7/site-packages/django/db/backends/mysql/base.py", line 37,」，去到這個文件裡面，把產生錯誤的36、37行註釋掉。
承上用virtualenv的話也是在這邊註釋掉（可是跑好幾次每次錯誤都不一樣囧直到某一次跑出來是這個錯誤才得以用同樣的方法解決）【/mnt/c/Users/st350/Desktop/virtual_env/quikok_env/lib/python3.8/site-packages/django/db/backends/mysql/base.py"】(by Annie)
    8. 終於可以成功執行了...然後顯示: 【You have 17 unapplied migration(s)】
    9. 根據這個印度人的作法: <https://www.youtube.com/watch?v=8gSjvehTqAk>，我們不makemigrations，直接python manage.py migrate，成功將資料migrate過去了。
<br>

###環境設定(Linux-Ubuntu)
1. 先依序輸入以下指令：<br>
    sudo apt-get install mysql-server<br>
    sudo apt install mysql-client<br>
    sudo apt install libmysqlclient-dev<br>
    sudo apt-get install net-tools 
2. 輸入以下指令看看是否有安裝成功：<br>
    sudo netstat -tap | grep mysql
3. 如果要讓遠端連線可以操控mysql資料庫的話，輸入以下指令：<br>
    sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf  (這是用nano開啟後面那個檔案的意思) <br>
    將其中的“bind-address = 127.0.0.1”註解掉，接著輸入ctrl+O進行存檔（記得按enter），接著輸入ctrl+X退出。
4. 接著輸入sudo mysql -u root   來進入mysql。
5. 輸入以下指令來設定root user的密碼（如果安裝過程已經輸入了，則可以跳過此一步驟），在QUIKOK專案中我們設定為0800：<br>
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql\_native\_password BY '你想設定的密碼';<br>
    exit;     << 跳出mysql terminal<br>
    service mysql restart    << 回到bash重新啟動mysql
6. 再從ubuntu store安裝MySQL Workbench就好囉。
7. 如果沒安裝MySQL Workbench，也可以透過這幾個常用指令來進行DB操作：<br>
    show databases;<br>
    create database your\_db\_name;<br>
    drop database your\_db\_name;