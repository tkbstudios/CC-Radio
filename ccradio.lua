base_url = "https://ccradio.tkbstudios.tk"
radio_URL = base_url.."/radio" -- you can add or remove the / after radio, doesn't change anything.
track_URL = base_url.."/track/" -- IMPORTANT TO HAVE LAST / !! Will lead to crash if not added
random_URL = base_url.."/radio/random"

-- Check if computer meets requirements
if term.isColor() == false then
    print("Please use an Advanced Computer!")
    return
end
-- APIs
os.loadAPI("json")
local dfpwm = require("cc.audio.dfpwm")

-- Initial terminal setup
term.setBackgroundColor(colors.black)
term.clear()

-- Get terminal information
termwidth, termheight = term.getSize()

-- Define term.write function for code optimization
local function writeErrorToTerm(text, color)
    local errorTitle = "An error occured!"
    term.setBackgroundColor(colors.blue)
    term.setTextColor(colors.red)
    term.clear()

    term.setCursorPos(16, 2)
    term.write(errorTitle)
    
    term.setCursorPos(16, termheight/2)
    term.write(text)
    term.setCursorPos(1, termheight)
    term.setBackgroundColor(colors.black)
    term.setTextColor(colors.white)
    return
end

local function writeCenteredToTerm(text, color)
    term.setTextColor(color)
    term.setCursorPos(termwidth/2-#text, termheight/2)
    term.write(text)
end

local function writeHorizontalCenteredToTerm(text, ypos, color)
    term.setTextColor(color)
    term.setCursorPos(termwidth/2-#text, ypos)
    term.write(text)
end

local function writeToTerm(text, xpos, ypos, color)
    term.setTextColor(color)
    term.setCursorPos(xpos, ypos)
    term.write(text)
end

print("Terminate the Currently Playing window to skip songs")
while true do
    os.sleep(0.3) -- prevent crash
    if multishell.getCount() == 1 then
        shell.run("speaker stop")
        local request = http.get(random_URL, {}, false)
        local response = request.readAll()
        print("Playing "..response)
        local URL = track_URL..response
        local command = "speaker play "..URL
        local speakerTabID = shell.openTab(command)
        multishell.setTitle(speakerTabID, "Currently Playing")
    end
end