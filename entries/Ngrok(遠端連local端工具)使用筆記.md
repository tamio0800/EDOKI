**Ngrok是一款可以讓其他user透過http public domain連到自己localhost的服務。**  
  
1. 首先先到官網 <https://ngrok.com/> 下載對應電腦環境的ngrok程式。  
2. 以windows搭配django為例，假設下載的路徑為download資料夾底下，確認它能不能正常使用:  
    1. 使用cmd，先cd至download資料夾，而後輸入**ngrok --help**，看是否有跳出使用說明，有的話代表成功，沒有的話檢查一下路徑是否有輸入錯誤。  
    2. 若使用bash其實也一樣，下載Linux使用版本後，可以直接執行該ngrok檔 --help，看是否有成功跳出使用說明，所以後續不多做Linux的使用說明版本。  
3. 在ngrok註冊帳號，取得authtoken，並在cmd中輸入**ngrok authtoken 你的token值**以啟動認證，注意指令中的ngrok需要是它所在的位置，官網中的範例圖在此:  
    <img src="https://lh6.googleusercontent.com/RfXbEmiRrVAZfRDF-KUmgqSVbWQ9Bcmejw2h7l1DqkskHBKWObz8-GnGp8ODssxaZB3qlT6gASzqbDumo3TqawgeKQOFSIBdlQIEEiQ">  
4. 接著開啟django專案，輸入**python manage.py runserver**開啟local端的伺服器連線，假設port為8000。  
5. 在cmd中輸入**ngrok http 8000**(注意這裡的ngrok也是它這個檔案所在的位置唷，會看到類似這樣的產出（黃色框處即是ngrok產生的虛擬網址）：  
    <img src="https://lh3.googleusercontent.com/0V-nhhVWN2g_2xOorteWuPDS-QEABgYf_lLetb5KxWC5wVof4amqgqGcg_xuV19fIYVBZvmxVs3ecpvvEpygFgXJhAOKI0NMoAnOWv4v">  
6. 以樂天派專案為例，如果要到ordertracking頁面的話，輸入以下網址即可:    
    <https://c5395ec3c3c7.ngrok.io/order_manage/ordertracking/>