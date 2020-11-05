<h3>VS Code & WSL 安裝與設定</h3>
1. 下載VS Code並完成安裝。
2. 在MS Store搜尋ubuntu，並點選下圖黃框安裝它:<br>
    <img src="https://lh6.googleusercontent.com/ASTtL_ydR-A-kunqeoldfuppGeXJu6u8I9oJRnqVydLjDJJyGnH4l2OsQtQt7fSK8Zdu26wgCIvXgY_bqTXZ1LnvrHCP9zr5Ab3seqh7"><br>
3. 安裝完成後從「開始」選單啟動ubuntu。 <br>
    1. 在這一步出現WslRegisterDistribution failed with error: 0x8007019e <br>
    2. 先用管理員身分開啟powershell <br>
    3. 輸入Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux <br>
    4. 等待它跑完後，輸入Y（會立即重新啟動電腦，有要儲存的東西記得先儲存）。<br>
    5. 重啟後，在「開始」那邊點選ubuntu圖示，就會開始安裝了。<br>
4. 啟動VS Code，右下角出現通知建議安裝Remote-WSL插件，跟著安裝即可。<br>
    1. 安裝完成後，點選最左下角的><圖示，應該可以看到畫面上方中間處可使用remote-wsl模式開啟new window，嘗試開啟看看確認是否安裝成功。<br>
    2. 如果有安裝成功，應該可以在那個new window的左下方看到「>< WSL: Ubuntu」的字眼。
<h3>(Mini) Conda安裝與設定</h3>
1. 關掉VS Code，在桌面新開一個conda\_temp資料夾。
    1. 點擊資料夾後，在上方address bar輸入wsl以開啟bash。<br>
    2. 先更新一下ubuntu:<br>
        sudo apt update <br>
        sudo apt upgrade <br>
    3. 輸入sudo apt-get install build-essential，下載不同程式語言的編譯器。<br>
        (我發現今年來越來越多人推miniconda，跟anaconda相比主要少了圖形化的介面，但該有的東西也都有，而且跟WSL結合的過程中比較不會有奇怪的衝突，所以這裡嘗試安裝miniconda。)<br> 
    4. 輸入wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh <br>
    5. 輸入sudo bash Miniconda3-latest-Linux-x86\_64.sh，接著一步一步安裝。  <br>
        第一個問題輸入: yes  <br>
        接著第二個問題，修改安裝路徑為 /home/YOUR\_USERNAME/miniconda3  (**很重要!!!**)  <br>
        第三個問題一樣: yes <br>
    6.  重新開啟bash後，輸入export PATH=”$PATH:/home/YOUR\_USERNAME/miniconda3/bin”以註冊路徑。
    7.  輸入conda init以便初始化，完成後重新開啟bash。
    8. 應該就會看見這個可愛的(base)了: <br>
    <img src="https://lh3.googleusercontent.com/pDErK2Eettzaxq-QfmTjNSTtocEr1yEyOhQgAY4wDc0CcFiS16g9SrsKeIS8LYRETvpjmLnaK8wu2f32hAq07WbvhCUwhyTkCD6lHVI"><br>
    9. 打開VS Code(WSL)，terminal(bash)也是一致的，成功囉~
<br>  

_**PS. 建議在VS Code下載GitLens插件，可以很清楚的看到誰改了哪些東西 & 怎麼改的。**_