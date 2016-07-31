wifi.setmode(wifi.STATION) -- seems to come out of the box in a different mode

if (wifi.sta.sethostname("NodeMCU") == true) then
    print("hostname was successfully changed")
else
    print("hostname was not changed")
end

wifi.sta.config("ATT226","3902845518")
wifi.sta.connect()
tmr.delay(1000000)   -- wait 1,000,000 us = 1 second
print(wifi.sta.status())
print(wifi.sta.getip())
