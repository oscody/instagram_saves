-- mpv script for play_saves.py: keys for like/next/previous and a log of what I watch.
--
-- play_saves.py passes two script options:
--   index: playlist_index.json, which says which playlist entries belong to which post
--   log:   watch_log.jsonl, one line per post when it ends or I move on (plus a line per like)
--
-- One post is one item: a carousel's slides are separate playlist entries, but next/previous
-- jump past the whole post and a like applies to the whole post.

local mp = require "mp"
local utils = require "mp.utils"
local options = require "mp.options"

local opts = { index = "", log = "" }
options.read_options(opts, "saves_log")

local posts = {}       -- from the index, in play order
local post_at = {}     -- playlist position (0 based) -> post number (1 based)
local image_seconds = 6

local current = nil    -- post number being shown
local watched = 0      -- seconds of the current post watched so far (not counting pauses)
local since = nil      -- mp.get_time() when the current stretch of watching began, nil while paused
local liked = false
local reached_end = false
local playing_pos = -1 -- playlist position of the file on screen

local function load_index()
    local file = io.open(opts.index, "r")
    if not file then
        mp.msg.error("cannot read index " .. opts.index)
        return
    end
    local data = utils.parse_json(file:read("*a"))
    file:close()
    image_seconds = data.image_seconds or image_seconds
    posts = data.posts
    for n, post in ipairs(posts) do
        for i = 0, post.count - 1 do
            post_at[post.first + i] = n
        end
    end
end

local function write_line(entry)
    local file = io.open(opts.log, "a")
    if not file then
        mp.msg.error("cannot write log " .. opts.log)
        return
    end
    file:write(utils.format_json(entry) .. "\n")
    file:close()
end

local function watched_now()
    if since then
        return watched + (mp.get_time() - since)
    end
    return watched
end

local function length_of(post)
    return post.video_s + post.images * image_seconds
end

-- Log the post I'm leaving. quitting: mpv is closing, which is not a verdict on the post.
local function finish_post(quitting)
    if not current then
        return
    end
    local post = posts[current]
    local seconds = watched_now()
    local length = length_of(post)
    local event
    if reached_end then
        event = "finished"
    elseif quitting then
        event = "quit"
    elseif seconds < length / 2 then
        event = "skip"
    else
        event = "partial"
    end
    write_line({
        shortcode = post.shortcode,
        event = event,
        watched_s = math.floor(seconds * 10 + 0.5) / 10,
        length_s = math.floor(length * 10 + 0.5) / 10,
        liked = liked,
        at = os.date("%Y-%m-%dT%H:%M:%S"),
    })
    current = nil
end

local function show_title(post, seconds)
    local heart = liked and "♥ " or ""
    mp.osd_message(heart .. post.title .. "\n@" .. post.author, seconds)
end

mp.register_event("file-loaded", function()
    playing_pos = mp.get_property_number("playlist-pos", -1)
    local n = post_at[playing_pos]
    if not n or n == current then
        return
    end
    finish_post(false)
    current = n
    watched = 0
    since = (not mp.get_property_bool("pause")) and mp.get_time() or nil
    liked = false
    reached_end = false
    show_title(posts[n], 3)
end)

mp.register_event("end-file", function(event)
    -- The last file of the post played to its end on its own.
    if current and event.reason == "eof" then
        local post = posts[current]
        if playing_pos == post.first + post.count - 1 then
            reached_end = true
        end
    end
end)

mp.observe_property("pause", "bool", function(_, paused)
    if not current then
        return
    end
    if paused and since then
        watched = watched + (mp.get_time() - since)
        since = nil
    elseif not paused and not since then
        since = mp.get_time()
    end
end)

mp.register_event("shutdown", function()
    finish_post(true)
end)

local function jump(step)
    if not current then
        return
    end
    local target = posts[current + step]
    if not target then
        mp.osd_message(step > 0 and "Last post" or "First post", 2)
        return
    end
    mp.set_property_number("playlist-pos", target.first)
end

local function like()
    if not current or liked then
        return
    end
    liked = true
    local post = posts[current]
    write_line({
        shortcode = post.shortcode,
        event = "like",
        watched_s = math.floor(watched_now() * 10 + 0.5) / 10,
        length_s = math.floor(length_of(post) * 10 + 0.5) / 10,
        liked = true,
        at = os.date("%Y-%m-%dT%H:%M:%S"),
    })
    mp.osd_message("♥ liked", 2)
end

local function info()
    if not current then
        return
    end
    local post = posts[current]
    mp.osd_message(post.title .. "\n@" .. post.author .. "\n\n" .. post.summary, 10)
end

local function open_link()
    if not current then
        return
    end
    local post = posts[current]
    write_line({ shortcode = post.shortcode, event = "open", url = post.url, at = os.date("%Y-%m-%dT%H:%M:%S") })
    mp.osd_message("Link saved to the log:\n" .. post.url, 4)
end

local function image_time(change)
    image_seconds = math.max(2, image_seconds + change)
    mp.set_property_number("image-display-duration", image_seconds)
    mp.osd_message("Photos and slides: " .. image_seconds .. " s", 2)
end

load_index()
mp.add_forced_key_binding("l", "saves-like", like)
mp.add_forced_key_binding("n", "saves-next", function() jump(1) end)
mp.add_forced_key_binding("RIGHT", "saves-next-arrow", function() jump(1) end)
mp.add_forced_key_binding("p", "saves-prev", function() jump(-1) end)
mp.add_forced_key_binding("LEFT", "saves-prev-arrow", function() jump(-1) end)
mp.add_forced_key_binding("i", "saves-info", info)
mp.add_forced_key_binding("o", "saves-open", open_link)
mp.add_forced_key_binding("+", "saves-longer", function() image_time(2) end)
mp.add_forced_key_binding("=", "saves-longer-eq", function() image_time(2) end)
mp.add_forced_key_binding("-", "saves-shorter", function() image_time(-2) end)
