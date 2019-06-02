Attribute VB_Name = "Module1"
Sub stockData():
    Dim ws As Worksheet
    For Each ws In Workbooks("Multiple_year_stock_data.xlsm").Worksheets
    ws.Select
    'loop through all the sheets in the workbook
    
    
    Dim ticker, currentTicker, nextTicker As String
    Dim openValue, closeValue As Double
    Dim stockVolume As Double
    Dim uniqueTickerRow As Long
    Dim lastrow As Long
    Dim yearlyChange As Double
    Dim percentChange As Double
    'declare variables
    
    Cells(1, 9).Value = "Ticker"
    Cells(1, 10).Value = "Yearly Change"
    Cells(1, 11).Value = "Percent Change"
    Cells(1, 12).Value = "Total Stock Volume"
    Cells(1, 16).Value = "Ticker"
    Cells(1, 17).Value = "Value"
    Cells(2, 15).Value = "Greatest % Increase"
    Cells(3, 15).Value = "Greatest % Decrease"
    Cells(4, 15).Value = "Greatest Total Volume"
    'Enter headers
    
    lastrow = Cells(Rows.Count, 1).End(xlUp).Row
    'Find last row in the sheet
    uniqueTickerRow = 2
    'establish counter for column that shows unique tickers
    
    stockVolume = 0
    'initialize counter for total stock volume
    openValue = Cells(2, 3).Value
    'opening price for the first stock ticker on the first day of trading
    
    For i = 2 To lastrow
    'start with index 2 since we have a header row
            currentTicker = Cells(i, 1).Value
            nextTicker = Cells(i + 1, 1).Value
            
            If currentTicker <> nextTicker Then
                stockVolume = stockVolume + Cells(i, 7).Value
                closeValue = Cells(i, 6).Value
                'as soon as ticker symbol changes closing value for the previous ticker is derived
    
                Range("i" & uniqueTickerRow).Value = currentTicker
                Range("l" & uniqueTickerRow).Value = stockVolume

                               
                If openValue <> 0 Then
                    percentChange = (closeValue - openValue) * 100 / openValue
                Else
                    percentChange = 0
                End If
                'this loop is created because in some instances the opening value of a stock is zero
                Range("k" & uniqueTickerRow).Value = percentChange
                
                yearlyChange = closeValue - openValue
                Range("j" & uniqueTickerRow).Value = closeValue - openValue
                
                If yearlyChange > 0 Then
                    Range("j" & uniqueTickerRow).Interior.ColorIndex = 4
                Else
                    Range("j" & uniqueTickerRow).Interior.ColorIndex = 3
                End If
                'this loop formats the cells of the column that shows yearly change in stock values
                
                uniqueTickerRow = uniqueTickerRow + 1
                stockVolume = 0
                openValue = Cells(i + 1, 3).Value
            Else
                stockVolume = stockVolume + Cells(i, 7).Value
            End If
    Next i
    
    lastrow = Cells(Rows.Count, 9).End(xlUp).Row
    'determining the last row in the unique ticker column
    
     Set rng1 = Range("l2:l" & lastrow)
     maxVolume = Application.WorksheetFunction.Max(rng1)
     'using maximum function to determine the maximum value from the range
     Cells(4, 17).Value = maxVolume
     
     For i = 2 To lastrow
        If Cells(i, 12).Value = maxVolume Then
            ticker = Cells(i, 9).Value
        End If
    Next i
    'this loop determines the ticker which has maximum volume
    Cells(4, 16).Value = ticker
    
        Set rng2 = Range("k2:k" & lastrow)
        maxPercentIncrease = Application.WorksheetFunction.Max(rng2)
        maxPercentDecrease = Application.WorksheetFunction.Min(rng2)
        Cells(2, 17).Value = maxPercentIncrease
        Cells(3, 17).Value = maxPercentDecrease
        'to determine the greatest percent increase and decrease
        
     For i = 2 To lastrow
        If Cells(i, 11).Value = maxPercentIncrease Then
            ticker = Cells(i, 9).Value
        End If
    Next i
    'determines ticker with greatest percent increase
        Cells(2, 16).Value = ticker
    
    For i = 2 To lastrow
        If Cells(i, 11).Value = maxPercentDecrease Then
            ticker = Cells(i, 9).Value
        End If
    Next i
    'determines ticker with greatest percent decrease
        Cells(3, 16).Value = ticker

Workbooks("Multiple_year_stock_data.xlsm").Activate
Next ws

End Sub





