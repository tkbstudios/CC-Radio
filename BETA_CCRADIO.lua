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

local function removeExtension(track)
    return string.gsub(track, "%.dfpwm$", "")
end

local function displayMainMenu()
    term.setBackgroundColor(colors.black)
    term.clear()
    writeCenteredToTerm("CCRadio", colors.white)
    writeHorizontalCenteredToTerm("1. Random Track", termheight/2 + 1, colors.yellow)
    writeHorizontalCenteredToTerm("2. Select Track", termheight/2 + 2, colors.yellow)
end

local function handleMainMenuInput()
    while true do
        local event, key = os.pullEvent("key")
        if key == keys.one then
            return "random"
        elseif key == keys.two then
            return "select"
        end
    end
end

local function displayTrackSelectionMenu(tracks, page)
    local itemsPerPage = termheight - 4
    local totalPages = math.ceil(#tracks / itemsPerPage)
    term.setBackgroundColor(colors.black)
    term.clear()
    writeCenteredToTerm("Track Selection", colors.white)
    for i = 1, itemsPerPage do
        local trackIndex = (page - 1) * itemsPerPage + i
        if trackIndex <= #tracks then
            local track = removeExtension(tracks[trackIndex])
            writeHorizontalCenteredToTerm(tostring(trackIndex) .. ". " .. track, i + 1, colors.yellow)
        end
    end
    writeHorizontalCenteredToTerm("Page " .. page .. " of " .. totalPages, termheight - 1, colors.cyan)
end


local function handleTrackSelectionInput(numTracks, totalPages)
    local currentPage = 1
    while true do
        local event, key = os.pullEvent("key")
        local num = tonumber(keys.getName(key))
        if num and num >= 1 and num <= numTracks then
            return num
        elseif key == keys.pageUp and currentPage > 1 then
            currentPage = currentPage - 1
            displayTrackSelectionMenu(tracks, currentPage)
        elseif key == keys.pageDown and currentPage < totalPages then
            currentPage = currentPage + 1
            displayTrackSelectionMenu(tracks, currentPage)
        end
    end
end



print("Terminate the Currently Playing window to skip songs")
while true do
    os.sleep(0.3) -- prevent crash
    if multishell.getCount() == 1 then
        displayMainMenu()
        local menuChoice = handleMainMenuInput()

        shell.run("speaker stop")
        local selectedTrack

        if menuChoice == "random" then
            local request = http.get(random_URL, {}, false)
            local response = request.readAll()
            selectedTrack = response
        elseif menuChoice == "select" then
            local request = http.get(base_url .. "/songs", {}, false)
            local response = request.readAll()
            local tracks = json.decode(response)
            local itemsPerPage = termheight - 4
            local totalPages = math.ceil(#tracks / itemsPerPage)
            displayTrackSelectionMenu(tracks, 1)
            local selectedIndex = handleTrackSelectionInput(#tracks, totalPages)
            selectedTrack = tracks[selectedIndex]
        end
            

        print("Playing " .. selectedTrack)
        local URL = track_URL .. selectedTrack
        local command = "speaker play " .. URL
        local speakerTabID = shell.openTab(command)
        multishell.setTitle(speakerTabID, "Currently Playing")
    end
end
