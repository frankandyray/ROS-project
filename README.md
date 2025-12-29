
Final Project 
戳氣球小車BalloonPopBot

這個專題在ROS中建立4個節點用來處理圖片資料接收、影像辨識、區域映射、UART通訊等功能，最後驅動期中的做的小車來達成氣球追蹤

  (1)	yolo8模型訓練
  
  這裡我們使用anaconda建立虛擬環境，先進行圖片與標籤的資料集做分割(訓練與測試8:2)，再將這些資料集丟給YOLO8模型做訓練，訓練完成後再把模型傳進樹梅派中，就可以使用了(使用pt檔)
    
  (2) smart_car_msgs(ros package)
  
  *這個package是為了BBOX2D.msg檔特別創建的，因為他只能透過ament_cmake編譯
  
  *還須修改CMakeList.txt與package.xml
  
  *接著在創建兩個msg檔(BBox2DArray.msg、BBox.msg)，可用於發布模型的輸出參數，BBox20只能傳一個辨識框的資訊，BBox2DArray.msg可傳多個
  
  (3)	smart_car(ros package)
    
  *這個就是我們執行4個節點傳輸的地方也需修改package大致與HW7相同，Setup.py則新增為4條

  *camera_node大致上與HW7作業一致，都是抓取圖片

  *yolo_node與HW7不同的地方是我一次發送多個辨識視窗的內容(HW7僅只有一個)，使用BBox2DArray.msg格式發佈到第二個topic

  *zone_mapping_node這裡從第二個topic那訂閱，並取的多組辨識框資訊，並取辨識框長+寬最大的出來(最近的氣球)，並算出他的中心點座標，再透過座標的X值來片段器在左中右哪一區，最後發佈判斷數字(0左邊,1中間,2右邊)到第三個節點
    
  *uart_node這個節點的目的是為了接收0,1,2數字並透過UART(USB)序列傳送到arduino端，但這裡為了克服鏡頭延遲，所以設定5秒鐘接收一次數值，發送則是只有arduino端主動發送請求字元(R)才會將暫存的訊號發送出去

  (4)	arduino控制
    
  *這裡的一開始會發送R的訊息請求，表示可以接收訊號，接著就透過讀取的數值判斷馬達要左轉、右轉或前進(左右轉持續運作200ms、直走持續運作800ms)再來會自動停車4秒，再接著發送下一筆接收請求，以此類推


