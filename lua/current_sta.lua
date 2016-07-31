--Get current Station configuration
ssid, password, bssid_set, bssid=wifi.sta.getconfig()
print("\nCurrent Station configuration:\nSSID : "..ssid
.."\nPassword  : "..password
.."\nBSSID_set  : "..bssid_set
.."\nBSSID: "..bssid.."\n")
ssid, password, bssid_set, bssid=nil, nil, nil, nil
