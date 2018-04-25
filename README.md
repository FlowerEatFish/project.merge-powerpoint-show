![version][1] ![license][2]

[1]: https://img.shields.io/badge/version-1.2-green.svg
[2]: https://img.shields.io/badge/license-GPLv3-blue.svg

## 初始介面：

![sample][3]

上述所有參數皆為初始狀態。

[3]: https://raw.githubusercontent.com/FlowerEatFish/project.tv-wall/master/public/image/sample.png

## 需求：

1. 使用 Microsoft PowerPoint 並設為預設開啟程式。

2. 確認啟動 Microsoft PowerPoint 時沒有彈出視窗（序號啟用通知、預設程式通知等）。

## 使用者手冊：

![guide][4]

[4]: https://raw.githubusercontent.com/FlowerEatFish/project.tv-wall/master/public/image/guide.png

1. 選擇簡報檔案放置的資料夾。如果資料夾裡面仍有另一個資料夾，不會檢查另一個資料夾裡面的檔案。

2. 設定「點擊『開始運行』後，等待幾秒後啟動 Microsoft PowerPoint」，以及「每隔幾秒切換至下一張投影片」。

3. 如果勾選此項，下一次執行程式時，自動運行（仍然需要等待幾秒後啟動 Microsoft PowerPoint）。

4. 如果勾選此項，於啟動 Microsoft PowerPoint 之前，會先刪除已過期的檔案。**（但不會跳出詢問視窗，而是自動刪除且不會丟到資源回收桶）**

   - 為避免剩下的檔案過少或是沒有檔案，亦可設置要保留**最近建立**的檔案數量。

## 錯誤排除：

![error-1][error-1]

解決：請確認目標資料夾是否含有簡報檔案，或資料夾路徑是否正確。

進階：目前可被讀取的副檔名為 .odp 及 .ppt* 。

其他：也有可能被清理功能設置的參數完全清除，造成沒有簡報檔案可以被讀取。

***

![error-2][error-2]

解決：請確認每一個簡報是否含有投影片。

**注意：只要至少一個簡報含有投影片，沒有投影片的其他簡報會被自動忽略，而不會有此錯誤訊息。**

***

![error-3][error-3]

解決：請先關閉全數 Microsoft PowerPoint 程式。

進階：main-slide.ppt 先前已被開啟，造成「唯讀」狀態，無法覆寫。

其他：也有可能是預設開啟程式不為 Microsoft PowerPoint 。

***

![error-4][error-4]

解決：再次運行即可。

**已知問題：程式僅在「投影片切換間隔秒數」一到才會進入檢查點，如果使用者自行關閉輪播運作，必須得等待「投影片切換間隔秒數」一到才能正式結束。**

***

![error-5][error-5]

解決：輸入半形數字、正整數，不含小數點、符號、以及其他非數字的字符。

***

[error-1]: https://raw.githubusercontent.com/FlowerEatFish/project.tv-wall/master/public/image/error-1.png
[error-2]: https://raw.githubusercontent.com/FlowerEatFish/project.tv-wall/master/public/image/error-2.png
[error-3]: https://raw.githubusercontent.com/FlowerEatFish/project.tv-wall/master/public/image/error-3.png
[error-4]: https://raw.githubusercontent.com/FlowerEatFish/project.tv-wall/master/public/image/error-4.png
[error-5]: https://raw.githubusercontent.com/FlowerEatFish/project.tv-wall/master/public/image/error-5.png

## 未來計劃：

- [ ] 取代刪除功能，將過期檔案移動（含覆寫）至另一資料夾。
- [ ] 設置釋放版本的歷史紀錄。
