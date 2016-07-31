if (wifi.sta.sethostname("NodeMCU") == true) then
    print("hostname was successfully changed")
else
    print("hostname was not changed")
end