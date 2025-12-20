# Beneath the House - A Text Adventure
# Converted from game.tapln

# Initialize persistent data for tracking endings
default persistent.endings_seen = set()

# Initialize variables
default current_music = None

# Custom screen shake for horror moments
transform shake:
    linear 0.1 xoffset 5
    linear 0.1 xoffset -5
    linear 0.1 xoffset 3
    linear 0.1 xoffset -3
    linear 0.1 xoffset 0

# Main entry point
label start:
    # Show a brief title card
    scene black with fade
    centered "{size=+20}BENEATH THE HOUSE{/size}"
    pause 2.0

    jump scene_start

# ============================================
# ACT I - NIGHT ONE
# ============================================

label scene_start:
    play music "audio/music/start.wav" fadeout 1.0 fadein 1.0
    scene bg_start with fade

    "You pull into the driveway at 7:43 PM. Late again. The porch light is on—Morgan remembered tonight."

    "Inside, the house smells like reheated soup. Something from a can. The TV murmurs from the living room."

    "You find Morgan on the couch, wrapped in the old blue blanket from your parents' house. She looks up when you come in. Tired, but present. A good day, then. You've learned to recognize them."

    "\"Hey. There's soup if you want some.\""

    "You drop your bag by the door. Ask about her day."

    "\"Actually decent.\" She shifts to make room for you, though you haven't sat yet. \"I found this online group. Support thing, for people with... you know. Chronic stuff. It's nice. Talking to people who get it.\""

    menu:
        "\"That's great. I'm glad you found people to talk to.\"":
            jump scene1_1
        "\"What kind of group? What do they talk about?\"":
            jump scene1_2
        "\"Just be careful with online stuff. Lots of weirdos out there.\"":
            jump scene1_3

label scene1_1:
    "Morgan smiles. It reaches her eyes—rare, these days. \"Yeah. Me too.\" She pulls the blanket tighter. \"They're really welcoming. No pity, no toxic positivity. Just... understanding.\""

    "You feel something loosen in your chest. Maybe you don't have to carry this alone."

    "Later, as you're heading to bed, Morgan calls out from the couch. \"Hey. Want to watch something? There's this documentary about deep-sea creatures. Supposed to be really good.\""

    "You have work early tomorrow. The kind of early that makes 6 AM feel like a personal insult."

    menu:
        "Stay and watch the documentary.":
            jump scene1_movie_stay
        "\"I'm sorry, I really need to sleep. Early morning.\"":
            jump scene1_movie_decline
        "\"Maybe something short? Like an episode of something?\"":
            jump scene1_movie_compromise

label scene1_2:
    "Morgan's expression flickers. Just for a second. \"Coping, mostly. Pain management. Acceptance.\" She shrugs. \"Normal stuff. Why?\""

    "\"Just curious.\""

    "\"Mm.\" She turns back to the TV. The openness from a moment ago has receded slightly. You're not sure why."

    "Later, as you're heading to bed, Morgan calls out from the couch. \"Hey. Want to watch something? There's this documentary about deep-sea creatures. Supposed to be really good.\""

    "You have work early tomorrow. The kind of early that makes 6 AM feel like a personal insult."

    menu:
        "Stay and watch the documentary.":
            jump scene1_movie_stay
        "\"I'm sorry, I really need to sleep. Early morning.\"":
            jump scene1_movie_decline
        "\"Maybe something short? Like an episode of something?\"":
            jump scene1_movie_compromise

label scene1_3:
    "Morgan's jaw tightens. \"I'm sick, not stupid.\""

    "\"That's not what I—\""

    "\"I know.\" She exhales. \"Sorry. I just... I finally found something that helps, and I don't want to defend it already.\""

    "The silence that follows has weight to it."

    "Later, as you're heading to bed, Morgan calls out from the couch. Her voice is softer now. \"Hey. Want to watch something? There's this documentary about deep-sea creatures. Supposed to be really good.\""

    "You have work early tomorrow. The kind of early that makes 6 AM feel like a personal insult."

    menu:
        "Stay and watch the documentary.":
            jump scene1_movie_stay
        "\"I'm sorry, I really need to sleep. Early morning.\"":
            jump scene1_movie_decline
        "\"Maybe something short? Like an episode of something?\"":
            jump scene1_movie_compromise

label scene1_movie_stay:
    play music "audio/music/peaceful.wav" fadeout 1.0 fadein 1.0
    scene bg_living_room_night with dissolve

    "You settle onto the couch beside her. Morgan makes a small, pleased sound and shifts closer, sharing the blanket."

    "The documentary is strange and beautiful—bioluminescent creatures pulsing in the dark, things that live where light never reaches."

    "\"Imagine living down there,\" Morgan says quietly. \"In all that pressure. All that darkness. And you just... adapt.\""

    "You're only half-watching. Mostly you're noticing how Morgan keeps scratching absently at her wrist. A new habit. The skin there looks raw."

    "When the credits roll, she's asleep against your shoulder. You carry her to bed, careful not to wake her. She weighs less than she should."

    jump night2_intro

label scene1_movie_decline:
    play music "audio/music/quiet.wav" fadeout 1.0 fadein 1.0
    scene bg_hallway_night with dissolve

    "\"I'm really sorry. I have that 6 AM—\""

    "\"It's okay.\" Morgan's voice is light, practiced. \"I understand.\""

    "But her eyes have already gone somewhere else. That look you've seen before—the one that says she expected this. That she's used to being left alone."

    "\"We'll do something this weekend,\" you offer."

    "\"Yeah.\" She turns back to the TV. \"Night.\""

    "You lie in bed for a long time, staring at the ceiling, listening to the muffled sounds of whatever she's watching. Wondering when every small moment started feeling like a test you're failing."

    jump night2_intro

label scene1_movie_compromise:
    play music "audio/music/peaceful.wav" fadeout 1.0 fadein 1.0
    scene bg_living_room_night with dissolve

    "You compromise on an old sitcom—something brainless and familiar. Morgan seems distracted the whole time, glancing at her phone occasionally."

    "When it buzzes, she smiles at whatever she sees. \"Group chat,\" she explains when she catches you looking. \"Someone shared a really good article.\""

    "\"About what?\""

    "\"Just... coping stuff.\" She locks the phone. \"Mind if we finish this tomorrow? I'm actually kind of tired.\""

    "You say goodnight, but something about the exchange leaves you unsettled. Not worried, exactly. Just... aware that something is shifting that you can't quite name."

    jump night2_intro

# ============================================
# ACT I - NIGHT TWO
# ============================================

label night2_intro:
    play music "audio/music/uneasy.wav" fadeout 1.0 fadein 1.0
    scene bg_house_exterior_dusk with fade

    pause 0.5

    "One week later."

    scene bg_living_room_dark with dissolve

    "You come home and the house feels different. The air is thick with something—incense, maybe. Earthy and unfamiliar. Sweet in a way that coats the back of your throat."

    "The living room is dark. No TV. No lights. Morgan is sitting on the floor, cross-legged, facing the window. Her back is to you."

    "She's more energetic than she's been in months. Practically vibrating with it."

    "\"You're home.\" She doesn't turn around. \"I've been thinking about something all day. About acceptance.\""

    "She stands, finally faces you. She's wearing something new—a pendant. A simple circle with a vertical line through it, hanging from a leather cord."

    menu:
        "\"That's new. Where'd you get it?\"":
            jump night2_pendant_ask
        "Say nothing about the pendant. Just listen.":
            jump night2_pendant_silent
        "\"Is that from your group?\"":
            jump night2_pendant_group

label night2_pendant_ask:
    "Morgan's hand goes to the pendant, protective. \"A friend gave it to me. From the group.\" She smiles, but there's something guarded in it. \"It's just a symbol. Helps me focus.\""

    "\"Focus on what?\""

    "\"On what matters.\" She turns away, moving toward the kitchen. \"The group has been talking about something interesting. About 'what's underneath.' How we spend so much energy fighting against things instead of accepting what's already there.\""

    menu:
        "\"Try me. What are they telling you?\"":
            jump night2_press
        "Let it go. She seems happy, and that's rare.":
            jump night2_let_go
        "\"This is starting to sound weird. Are you okay?\"":
            jump night2_concern

label night2_pendant_silent:
    "You don't mention the pendant. Your eyes trace its shape—circle, line—and file it away. Morgan seems to appreciate that you don't ask. Or maybe she doesn't notice at all."

    "\"The group has been talking about something interesting,\" she continues. \"About 'what's underneath.' How we spend so much energy fighting against things instead of accepting what's already there.\""

    "She looks at you expectantly. Waiting for a reaction."

    menu:
        "\"Try me. What are they telling you?\"":
            jump night2_press
        "Let it go. She seems happy, and that's rare.":
            jump night2_let_go
        "\"This is starting to sound weird. Are you okay?\"":
            jump night2_concern

label night2_pendant_group:
    "Morgan stiffens slightly. \"Why do you say it like that?\""

    "\"Like what?\""

    "\"Like you think they're... I don't know. Selling me something.\" She shakes her head. \"It's just a symbol. It represents—\" She stops herself. \"Never mind. You wouldn't understand yet.\""

    "The word 'yet' hangs in the air."

    "\"The group has been talking about something interesting,\" she continues, her voice lighter now. Forced casual. \"About 'what's underneath.' How we spend so much energy fighting against things instead of accepting what's already there.\""

    menu:
        "\"Try me. What are they telling you?\"":
            jump night2_press
        "Let it go. She seems happy, and that's rare.":
            jump night2_let_go
        "\"This is starting to sound weird. Are you okay?\"":
            jump night2_concern

label night2_press:
    play music "audio/music/tense.wav" fadeout 1.0 fadein 1.0

    "Morgan's smile doesn't waver, but her eyes go flat. \"You wouldn't understand. Not yet.\""

    "\"That's not an answer.\""

    "\"It's the only one I have.\" She moves past you toward the stairs. \"I'm tired. We can talk more tomorrow.\""

    "But tomorrow, she won't mention it. And you'll be too afraid to ask."

    scene bg_bedroom_dark with fade

    "That night, you wake at 3 AM to the sound of footsteps upstairs. Not walking—pacing. Back and forth, back and forth. Then they stop. Somewhere near the water heater closet."

    menu:
        "Get up and check on Morgan.":
            jump night2_investigate
        "Call out from bed. \"Morgan? You okay?\"":
            jump night2_call_out
        "Stay in bed. It's probably nothing.":
            jump night2_ignore

label night2_let_go:
    "You let it go. She seems happy—genuinely happy—for the first time in months. Whatever this group is doing for her, it's working. Isn't that what matters?"

    "\"I'm glad you found something that helps,\" you say."

    "Morgan beams. \"I knew you'd understand.\""

    "But later, lying in bed, you wonder if understanding and enabling are the same thing."

    scene bg_bedroom_dark with fade

    "At 3 AM, you wake to the sound of footsteps upstairs. Not walking—pacing. Back and forth, back and forth. Then they stop. Somewhere near the water heater closet."

    menu:
        "Get up and check on Morgan.":
            jump night2_investigate
        "Call out from bed. \"Morgan? You okay?\"":
            jump night2_call_out
        "Stay in bed. It's probably nothing.":
            jump night2_ignore

label night2_concern:
    play music "audio/music/tense.wav" fadeout 1.0 fadein 1.0

    "\"This is starting to sound like—\""

    "\"Like what?\" Morgan's voice sharpens. \"Like a cult? Like I'm too stupid to know when I'm being manipulated?\""

    "\"That's not what I said.\""

    "\"It's what you meant.\" She takes a breath. Forces calm. \"I'm sorry. I just... I finally feel like I'm getting somewhere. Like I'm not just waiting to die.\""

    "The words hit you like a slap."

    "\"Morgan—\""

    "\"I'm tired.\" She's already heading for the stairs. \"Goodnight.\""

    scene bg_bedroom_dark with fade

    "That night, you wake at 3 AM to the sound of footsteps upstairs. Not walking—pacing. Back and forth, back and forth. Then they stop. Somewhere near the water heater closet."

    menu:
        "Get up and check on Morgan.":
            jump night2_investigate
        "Call out from bed. \"Morgan? You okay?\"":
            jump night2_call_out
        "Stay in bed. It's probably nothing.":
            jump night2_ignore

label night2_investigate:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_hallway_dark with dissolve

    "You ease out of bed, feet cold on the hardwood. The hallway is dark. Silent now."

    "Morgan's door is closed. You press your ear to it—nothing. Just the soft rhythm of breathing. Asleep."

    "But the footsteps were real. You know they were."

    "You stand in the hallway for a long moment, listening. A faint draft brushes your ankles. Coming from... where? The water heater closet? But that's an interior wall. There's nowhere for a draft to come from."

    "You go back to bed. You don't sleep."

    jump night3_intro

label night2_call_out:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "\"Morgan?\" Your voice sounds too loud in the darkness. \"You okay?\""

    "Silence. Then, from upstairs: \"Go back to sleep.\""

    "Her voice is strange. Thick. Like she's speaking through water."

    "\"What are you doing up there?\""

    "A long pause. \"Just... thinking. Go back to sleep.\""

    "You lie there, heart pounding, listening to the silence where footsteps used to be. Eventually, you drift off."

    "Your dreams are full of circles. Concentric rings, spiraling down and down and down."

    jump night3_intro

label night2_ignore:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "Old houses make noises. That's what you tell yourself. Old houses settle and creak and sound like footsteps when you're half-asleep and already unsettled."

    "You pull the blanket higher. Close your eyes."

    "The footsteps don't return. But you swear, just before you drift off, you feel something. A warmth. Like breath on the back of your neck."

    "There's no one there when you turn around."

    jump night3_intro

# ============================================
# ACT I - NIGHT THREE
# ============================================

label night3_intro:
    play music "audio/music/tension.wav" fadeout 1.0 fadein 1.0
    scene bg_kitchen_evening with fade

    "The next night, everything is different."

    "You come home and the house is silent. No TV. No music. No incense. Just stillness."

    "Morgan is sitting at the kitchen table, hands folded in front of her. Waiting."

    "Her face is calm. Too calm. The kind of peace that feels practiced, like a mask made of serenity."

    "\"Sit down,\" she says. \"I need to tell you something.\""

    "You sit. The chair scrapes too loud in the quiet."

    "\"I've been chosen,\" Morgan says. Her eyes are bright, feverish. \"The Threshold Assembly has shown me what waits below. I'm not afraid anymore.\""

    "She reaches across the table. Her hand is ice cold."

    "\"The illness isn't punishment. It's preparation.\""

    menu:
        "\"This is insane. You're in a cult.\"":
            jump night3_anger
        "\"You're scaring me. Please, just talk to me.\"":
            jump night3_fear
        "\"Let's see another doctor. A specialist. Please.\"":
            jump night3_bargain
        "Say nothing. Just listen.":
            jump night3_silent

label night3_anger:
    "\"A cult? That's what you think?\" Morgan's voice is gentle, pitying. That's almost worse than anger."

    "\"You're being manipulated. These people are taking advantage of you because you're sick and scared and—\""

    "\"I'm not scared anymore. That's the point.\" She squeezes your hand, cold fingers pressing."

    "\"When I'm gone, don't look for me.\""

    "Your heart stops. \"What do you mean, 'when you're gone'?\""

    "\"But if you do—\" She pauses. Seems to catch herself. \"Never mind.\""

    menu:
        "\"If I do, what? Finish the sentence.\"":
            jump night3_press_gone
        "\"You're not going anywhere.\"":
            jump night3_denial
        "\"I'm calling someone. A doctor. This isn't right.\"":
            jump night3_call_help

label night3_fear:
    "Morgan's expression softens. For a moment, she looks like herself again—your sibling, tired and sick and scared."

    "\"I know,\" she whispers. \"I know I'm scaring you. But I need you to understand—I'm not running from something. I'm running toward it.\""

    "She squeezes your hand."

    "\"When I'm gone, don't look for me.\""

    "The words don't make sense. \"Gone where? Morgan, what are you—\""

    "\"But if you do—\" She stops. Shakes her head. \"Never mind. It doesn't matter.\""

    menu:
        "\"If I do, what? Finish the sentence.\"":
            jump night3_press_gone
        "\"You're not going anywhere.\"":
            jump night3_denial
        "\"I'm calling someone. A doctor. This isn't right.\"":
            jump night3_call_help

label night3_bargain:
    "\"We haven't tried everything. There are specialists, clinical trials—\""

    "\"Stop.\" Morgan's voice is firm but not unkind. \"I've accepted what's happening. You should too.\""

    "\"I can't accept losing you.\""

    "\"You won't.\" She smiles, strange and serene. \"Not really. Not the way you think.\""

    "She takes your hand."

    "\"When I'm gone, don't look for me. But if you do—\" A pause. Her eyes flicker toward the ceiling. Toward the upstairs hallway. \"Never mind.\""

    menu:
        "\"If I do, what? Finish the sentence.\"":
            jump night3_press_gone
        "\"You're not going anywhere.\"":
            jump night3_denial
        "\"I'm calling someone. A doctor. This isn't right.\"":
            jump night3_call_help

label night3_silent:
    "You say nothing. Just listen. Watch. Morgan seems to appreciate this. Or maybe she's beyond caring about your reaction."

    "\"They showed me what's underneath,\" she continues. \"Under the fear. Under the pain. Under... everything.\""

    "Her eyes are distant, focused on something you can't see."

    "\"When I'm gone, don't look for me.\""

    "The words don't land right. They feel rehearsed."

    "\"But if you do—\" She stops. Looks at you—really looks—for the first time all night. \"Never mind. You probably won't.\""

    menu:
        "\"If I do, what? Finish the sentence.\"":
            jump night3_press_gone
        "\"You're not going anywhere.\"":
            jump night3_denial
        "\"I'm calling someone. A doctor. This isn't right.\"":
            jump night3_call_help

label night3_press_gone:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "Morgan holds your gaze for a long moment. Then, quietly: \"Follow the warm air.\""

    "\"What does that mean?\""

    "But she's already standing, already moving toward the stairs. \"I'm tired. Let's talk tomorrow.\""

    scene bg_hallway_tapestry with dissolve

    "Before you go to bed, you notice something new in the upstairs hallway. A large woven tapestry, hung near the water heater closet. Abstract patterns in deep reds and browns."

    "\"For energy flow,\" Morgan explains when she catches you looking. \"It helps balance the space.\""

    menu:
        "Examine the tapestry closely.":
            jump night3_examine_tapestry
        "Accept the explanation.":
            jump night3_accept_tapestry
        "\"This is getting out of hand. What are you hiding?\"":
            jump night3_confront_tapestry

label night3_denial:
    "\"You're not going anywhere.\" You say it like a command. Like you have any control over this. Over anything."

    "Morgan just smiles. Sad and patient. The way you might smile at a child who doesn't understand death yet."

    "\"Okay,\" she says. \"Sure.\""

    "She stands. \"I'm tired. Let's talk tomorrow.\""

    scene bg_hallway_tapestry with dissolve

    "Before you go to bed, you notice something new in the upstairs hallway. A large woven tapestry, hung near the water heater closet. Abstract patterns in deep reds and browns."

    "\"For energy flow,\" Morgan says, appearing behind you. \"It helps balance the space.\""

    menu:
        "Examine the tapestry closely.":
            jump night3_examine_tapestry
        "Accept the explanation.":
            jump night3_accept_tapestry
        "\"This is getting out of hand. What are you hiding?\"":
            jump night3_confront_tapestry

label night3_call_help:
    "\"I'm calling someone. This isn't—you need help. Real help.\""

    "\"I have real help.\" Morgan stands, her chair scraping back. \"The kind you can't give me. The kind no doctor can.\""

    "\"Morgan, please—\""

    "\"I'm tired.\" Her voice is final. \"We can talk tomorrow. Or not.\""

    "She heads for the stairs. You stand in the empty kitchen, phone in hand, not knowing who to call. Who would believe this?"

    scene bg_hallway_tapestry with dissolve

    "Before bed, you notice something new in the upstairs hallway. A large woven tapestry, hung near the water heater closet. Abstract patterns in deep reds and browns."

    "\"Energy flow,\" Morgan says from her doorway. \"It helps balance the space.\""

    menu:
        "Examine the tapestry closely.":
            jump night3_examine_tapestry
        "Accept the explanation.":
            jump night3_accept_tapestry
        "\"This is getting out of hand. What are you hiding?\"":
            jump night3_confront_tapestry

label night3_examine_tapestry:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "You step closer. Run your hand along the fabric. It's heavier than it looks. Warmer, too—like it's been hanging in sunlight, though there are no windows here."

    "The tapestry covers more wall than necessary. The edges overlap, hiding... what? The water heater closet door should be visible. It isn't."

    "\"Goodnight,\" Morgan says, and closes her door."

    "You stand in the hallway a long time, your hand pressed against the warm fabric, trying to convince yourself you don't feel a draft behind it. Breathing slowly from somewhere you can't see."

    jump night4_gone

label night3_accept_tapestry:
    play music "audio/music/uneasy.wav" fadeout 1.0 fadein 1.0

    "\"Okay,\" you say. Because what else can you say? It's fabric on a wall. Weird, but harmless. Right?"

    "Morgan smiles. \"Goodnight.\""

    "\"Goodnight.\""

    "But you don't sleep well. You dream of walls that breathe. Of doors that open from the inside."

    jump night4_gone

label night3_confront_tapestry:
    play music "audio/music/tension.wav" fadeout 1.0 fadein 1.0

    "\"What's behind this?\" You reach for the edge of the tapestry."

    "Morgan's hand catches your wrist. Her grip is stronger than it should be."

    "\"Please.\" Her voice is barely a whisper. \"Not yet. I'm not ready.\""

    "\"Ready for what?\""

    "But she's already letting go. Already retreating to her room."

    "\"Goodnight,\" she says. The door closes."

    "You stand alone in the hallway, staring at the tapestry, feeling the warmth bleeding through the fabric. Telling yourself it's the water heater. That's all. Just the water heater."

    jump night4_gone

# ============================================
# ACT II - THE DISAPPEARANCE
# ============================================

label night4_gone:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_house_dark with fade

    "You come home the next night. The house is dark. Silent. Wrong."

    "No lights. No TV murmur. No soup smell. Just emptiness pressing against every surface."

    "\"Morgan?\" Your voice echoes. No answer."

    "You check the living room. The kitchen. The backyard. Nothing."

    "Her medication is on the counter. Her phone on the nightstand. Her shoes by the door."

    "But Morgan is gone."

    menu:
        "Check her bedroom first.":
            jump night4_search_bedroom
        "Check the bathroom—fear twisting in your gut.":
            jump night4_search_bathroom
        "Go straight to the backyard.":
            jump night4_search_backyard

label night4_search_bedroom:
    scene bg_bedroom_empty with dissolve

    "Her bed is made. Not slept in. The pendant is gone—the only thing missing."

    "On her nightstand, a book lies open. Not a book you recognize. Handwritten. The page shows a symbol you've seen before: circle, vertical line. And words in a language you don't recognize."

    "After thirty minutes of searching, calling her phone, walking the neighborhood—nothing. She's gone. Vanished. As if she was never here at all."

    menu:
        "Call 911 immediately.":
            jump night4_call_911
        "Call Elena, her former caretaker.":
            jump night4_call_elena
        "Drive around the neighborhood looking.":
            jump night4_search_drive

label night4_search_bathroom:
    scene bg_bathroom_empty with dissolve

    "Your heart pounds as you push open the door. Empty. No one there."

    "You sag against the doorframe, relief and confusion warring in your chest. She's not here. But she's not... she didn't..."

    "You search the rest of the house. Nothing. No sign of struggle. No note. Just absence."

    "Her medication untaken. Her phone uncharged. Her shoes by the door."

    "After thirty minutes of searching, calling, walking the neighborhood—nothing. She's vanished."

    menu:
        "Call 911 immediately.":
            jump night4_call_911
        "Call Elena, her former caretaker.":
            jump night4_call_elena
        "Drive around the neighborhood looking.":
            jump night4_search_drive

label night4_search_backyard:
    scene bg_backyard_night with dissolve

    "The backyard is empty. Moonlight on dead grass. The old swing set from childhood, rusted and still."

    "You circle the house. Check the shed. Nothing."

    "She's not outside. She's not inside. She's just... gone."

    "After thirty minutes of searching, calling her phone, walking the neighborhood—nothing. Vanished. Without shoes. Without medication. Without a trace."

    menu:
        "Call 911 immediately.":
            jump night4_call_911
        "Call Elena, her former caretaker.":
            jump night4_call_elena
        "Drive around the neighborhood looking.":
            jump night4_search_drive

label night4_call_911:
    play music "audio/music/somber.wav" fadeout 1.0 fadein 1.0
    scene bg_living_room_police with dissolve

    "The police arrive within the hour. They take notes. Ask questions. Look at you with that practiced sympathy that means they've seen this before."

    "Missing persons. Chronically ill."

    "\"We'll do everything we can,\" they say."

    "You know what that means."

    jump search_montage

label night4_call_elena:
    play music "audio/music/somber.wav" fadeout 1.0 fadein 1.0
    scene bg_living_room_night with dissolve

    "Elena answers on the third ring. When you tell her, her breath catches."

    "\"Oh no. Oh no, no.\""

    "\"You knew something was wrong.\""

    "\"I... I noticed things. The last few weeks. She was different. Drawing things. Talking about 'going home.'\" She pauses. \"You should call the police. Now.\""

    "You do. They arrive within the hour. Take notes. Ask questions. Promise to do everything they can."

    jump search_montage

label night4_search_drive:
    play music "audio/music/somber.wav" fadeout 1.0 fadein 1.0
    scene bg_car_night with dissolve

    "You drive for hours. Every street. Every parking lot. The hospital. The park. The old church she used to like. Nothing."

    "Eventually, you have to admit it. This isn't something you can fix with driving in circles."

    "You call the police. They arrive. They ask questions. They look at you with sympathy you don't want."

    jump search_montage

label search_montage:
    scene bg_police_station with fade

    "Two weeks blur together. Police interviews. Search parties. Flyers on every telephone pole in a five-mile radius."

    "Detective Marsh leads the investigation. He's kind, thorough, and increasingly pessimistic with each passing day."

    "They investigate the Threshold Assembly. Find a defunct website. A P.O. box that leads nowhere."

    "\"It's like they never existed,\" Marsh tells you. \"Except in her computer history. And a few others like her.\""

    "Others. Like Morgan. All missing. All with chronic illnesses. All vanished without a trace."

    jump search_marsh_interview

label search_marsh_interview:
    "Detective Marsh sits across from you. Coffee cups and case files between you."

    "\"I need to ask about Morgan's mental state,\" he says. \"In the weeks before she disappeared.\""

    menu:
        "Tell him everything—the cult, the pendant, the strange behavior.":
            jump search_tell_all
        "Downplay it. \"She was sick, but not crazy.\"":
            jump search_downplay
        "Withhold the details about the pendant and 'what's underneath.'":
            jump search_withhold

label search_tell_all:
    "You tell him everything. The support group. The pendant. The incense and sitting in the dark. \"What's underneath.\" The tapestry. Follow the warm air."

    "Marsh writes it all down. His expression doesn't change, but you can see it in his eyes—he thinks this is grief talking. Delusion."

    "\"We'll look into it,\" he says."

    "He doesn't believe you. But at least it's on record."

    jump search_elena_call

label search_downplay:
    "\"She was sick,\" you say. \"Chronic illness. Pain, fatigue—it wears on you. But she wasn't... she wasn't unstable. She was just looking for something to help.\""

    "Marsh nods, writes something down."

    "\"These support groups—sometimes they give people hope where medicine can't. Sometimes that hope leads them to make... decisions.\""

    "He doesn't say suicide. Doesn't have to."

    "\"She didn't hurt herself,\" you say. Certain, even if you don't know why. \"She went somewhere.\""

    jump search_elena_call

label search_withhold:
    "You tell him most of it. The support group. The change in behavior."

    "But you don't mention the pendant. Don't mention \"what's underneath\" or the warm air or the way the tapestry pulsed with heat."

    "Those things are yours. Clues you're not ready to share. Evidence that sounds crazy when you say it out loud."

    "Marsh seems satisfied. \"We're doing everything we can,\" he says."

    "You believe him. You just don't think it will be enough."

    jump search_elena_call

label search_elena_call:
    scene bg_living_room_day with dissolve

    "Elena calls you a week later."

    "\"I need to tell you something,\" she says. \"About Morgan. In the weeks before... before. She was drawing something. Obsessively. Whenever you weren't home.\""

    menu:
        "\"What was she drawing?\"":
            jump elena_describe
        "\"Do you still have any of the drawings?\"":
            jump elena_drawings
        "\"Did she ever mention the Threshold Assembly to you?\"":
            jump elena_assembly

label elena_describe:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "Elena is quiet for a moment."

    "\"Tunnels,\" she says finally. \"Concentric circles, going down. Like a spiral. And at the bottom—\" Her voice catches. \"Something. I couldn't tell what. She wouldn't let me look for long.\""

    "Tunnels. Going down. You think about the warm air. The tapestry. The water heater closet that suddenly seems much more significant."

    jump funeral

label elena_drawings:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "\"I have one,\" Elena says. \"She threw most of them away, but I saved one. It was just so... detailed. I thought maybe a doctor should see it.\""

    "She sends you a photo."

    "The drawing is exactly what you feared. Concentric circles spiraling downward. A tunnel that goes deeper than any tunnel should. And at the bottom, something formless and waiting."

    "Your hands shake as you look at it."

    jump funeral

label elena_assembly:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "\"The Threshold Assembly?\" Elena sounds confused. \"No. Never by name. But she talked about 'the group.' About how they understood her in ways no one else could.\""

    "She pauses."

    "\"She said they showed her something. Something under the house. I thought she meant... metaphorically. The subconscious or something.\""

    "Under the house. The words echo."

    "\"Elena,\" you say slowly. \"Did Morgan ever mention anything about tunnels?\""

    "Silence. Then: \"She was drawing them. For weeks. Tunnels going down.\""

    jump funeral

label funeral:
    play music "audio/music/grief.wav" fadeout 1.0 fadein 1.0
    scene bg_cemetery with fade

    "Two weeks pass. No body is found. The search is called off."

    "Morgan is declared dead."

    "The funeral is small. A handful of people who knew her from before she got sick. Some coworkers. Elena, crying quietly in the back. Detective Marsh, standing at the edges, watching."

    "The casket is empty. A symbolic burial for someone who simply ceased to exist."

    "Afterward, a stranger approaches you. Well-dressed. Calm."

    "They offer condolences. \"Morgan spoke very highly of you,\" they say. \"They wanted you to have this.\""

    "They hand you an envelope."

    menu:
        "Take it and open it immediately.":
            jump funeral_open_now
        "Take it but wait until later.":
            jump funeral_open_later
        "\"Who the hell are you?\"":
            jump funeral_refuse

label funeral_open_now:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "You tear it open right there, fingers trembling."

    "Inside is a single piece of paper. A hand-drawn map of your house's second floor. An X marks the water heater closet."

    "On the back, written in Morgan's handwriting: \"THE DOOR OPENS FROM INSIDE.\""

    "When you look up, the stranger is gone. Vanished into the crowd of mourners. As if they were never there at all."

    menu:
        "Show the map to Detective Marsh.":
            jump funeral_show_marsh
        "Keep it to yourself.":
            jump funeral_keep_secret
        "Burn it.":
            jump funeral_burn

label funeral_open_later:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_living_room_night with dissolve

    "You pocket the envelope. Wait until you're home, alone, before opening it."

    "Inside is a single piece of paper. A hand-drawn map of your house's second floor. An X marks the water heater closet."

    "On the back, in Morgan's handwriting: \"THE DOOR OPENS FROM INSIDE.\""

    "You stare at the words for a long time. Follow the warm air. The door opens from inside. It's starting to make a terrible kind of sense."

    menu:
        "Show the map to Detective Marsh.":
            jump funeral_show_marsh
        "Keep it to yourself.":
            jump funeral_keep_secret
        "Burn it.":
            jump funeral_burn

label funeral_refuse:
    play music "audio/music/tension.wav" fadeout 1.0 fadein 1.0

    "\"Who are you? How do you know Morgan?\""

    "The stranger just smiles. Patient. Unbothered."

    "\"Someone who understands what Morgan was going through. Better than most.\""

    "They press the envelope into your hand before you can refuse again."

    "\"When you're ready,\" they say. \"You'll understand.\""

    "They walk away. By the time you think to follow, they've disappeared into the crowd."

    "The envelope feels warm in your hand."

    scene bg_living_room_night with dissolve

    "You open it later, alone. A map of your house. An X on the water heater closet. And on the back: \"THE DOOR OPENS FROM INSIDE.\""

    menu:
        "Show the map to Detective Marsh.":
            jump funeral_show_marsh
        "Keep it to yourself.":
            jump funeral_keep_secret
        "Burn it.":
            jump funeral_burn

label funeral_show_marsh:
    play music "audio/music/somber.wav" fadeout 1.0 fadein 1.0
    scene bg_police_station with dissolve

    "Marsh looks at the map for a long time."

    "\"This could be evidence,\" he says finally. \"Of what, I don't know. But I'll have someone check out the water heater closet.\""

    "They do. They find nothing. Just a closet. Just a water heater."

    "Marsh calls you, apologetic. \"I'm sorry. I know you were hoping for answers.\""

    "You hang up. Stare at the tapestry still hanging in the hallway."

    "They didn't look behind it. They didn't feel the warmth."

    jump months_later

label funeral_keep_secret:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "You keep the map. Fold it carefully. Put it in your nightstand drawer."

    "Some things aren't meant for police reports. Some things you have to understand yourself first."

    "The door opens from inside. You think about that for days. Weeks. What kind of door? And what's on the other side?"

    jump months_later

label funeral_burn:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_fireplace with dissolve

    "You hold the map over a flame. Watch it curl and blacken."

    "Some knowledge is dangerous. Some doors should stay closed."

    "But even as the paper turns to ash, you can't burn the words from your memory."

    "THE DOOR OPENS FROM INSIDE."

    "You dream about it for weeks. A door that wasn't there. A warmth that shouldn't exist. Something waiting on the other side."

    jump months_later

# ============================================
# ACT III - THE HAUNTED MONTHS
# ============================================

label months_later:
    play music "audio/music/emptiness.wav" fadeout 1.0 fadein 1.0
    scene bg_house_day_grey with fade

    "Three months pass. The world moves on. You don't."

    "You live in a fog. Work. Home. Sleep. Repeat."

    "The house feels different now—emptier, obviously, but something else too. Like it's watching. Waiting."

    "Morgan's things are still everywhere. You can't bring yourself to pack them up. Can't bring yourself to stay, either."

    "Most nights you sleep on the couch, TV murmuring, trying not to think about the upstairs hallway. The tapestry you still haven't moved."

    menu:
        "Drinking. The nights are easier with something to blur them.":
            jump coping_drinking
        "Working obsessively. Filling every hour.":
            jump coping_working
        "Going through Morgan's things, looking for answers.":
            jump coping_searching
        "Avoiding the house entirely.":
            jump coping_avoiding

label coping_drinking:
    scene bg_living_room_night with dissolve

    "The bottle helps. Blurs the edges. Makes the silence feel less like an accusation."

    "You drink until you can't remember why you're drinking, and that's the point."

    scene bg_bedroom_dark with fade

    "One night, you wake at 3:17 AM. Stone sober, impossibly, heart pounding."

    "There's a sound coming from upstairs. Rhythmic. Persistent. Not footsteps."

    "Something like knocking. From inside the walls."

    menu:
        "Investigate immediately.":
            jump wrongness_investigate
        "Pull the covers over your head. You're imagining it.":
            jump wrongness_deny
        "Record it on your phone.":
            jump wrongness_record

label coping_working:
    scene bg_office_night with dissolve

    "You take on extra shifts. Volunteer for overtime. Stay late, come early."

    "Anything to avoid the empty house and its waiting silence."

    "Your boss asks if you're okay. You say yes. Neither of you believes it."

    "One night you come home, exhausted, planning to collapse into bed without thinking."

    "Instead, you freeze in the doorway."

    "There's a sound coming from upstairs. Rhythmic. Persistent. Not footsteps."

    "Something like knocking. From inside the walls."

    menu:
        "Investigate immediately.":
            jump wrongness_investigate
        "Tell yourself you're imagining it. Go to bed.":
            jump wrongness_deny
        "Record it on your phone.":
            jump wrongness_record

label coping_searching:
    scene bg_bedroom_searching with dissolve

    "You go through everything. Every drawer, every journal, every scrap of paper."

    "Looking for something—you're not sure what. Answers. Explanations. Proof that you're not losing your mind."

    "You find her old drawings. The tunnels. The circles going down. The thing at the bottom that might be a shape or might be nothing at all."

    scene bg_bedroom_dark with fade

    "One night, you fall asleep at her desk. Wake at 3:17 AM to a sound."

    "Rhythmic. Persistent. Not footsteps."

    "Something like knocking. From inside the walls."

    menu:
        "Investigate immediately.":
            jump wrongness_investigate
        "Tell yourself you're imagining it.":
            jump wrongness_deny
        "Record it on your phone.":
            jump wrongness_record

label coping_avoiding:
    scene bg_car_night with dissolve

    "You stay late at work. Sleep on friends' couches. Do anything to avoid the house and its terrible silence."

    "When you do go home, you move quickly, eyes averted, in and out before the walls can notice you."

    "But eventually you run out of excuses. Run out of couches."

    scene bg_bedroom_dark with fade

    "One night, you have to stay. And at 3:17 AM, you wake to a sound."

    "Rhythmic. Persistent. Not footsteps."

    "Something like knocking. From inside the walls."

    menu:
        "Investigate immediately.":
            jump wrongness_investigate
        "Tell yourself you're imagining it.":
            jump wrongness_deny
        "Record it on your phone.":
            jump wrongness_record

label wrongness_investigate:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0
    scene bg_hallway_dark with dissolve

    "You creep up the stairs, heart hammering. The knocking continues—rhythmic, patient. It's coming from behind the tapestry. You're certain now."

    "When you reach the hallway, it stops. Just silence. Just the warm air bleeding through the fabric."

    "You stand there for a long time, hand raised, almost touching the tapestry. Almost pulling it aside."

    "You don't. Not yet. You go back to bed. You don't sleep."

    jump wrongness_pendant

label wrongness_deny:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0

    "Old houses. Pipes. Settling foundations. That's all it is."

    "You pull the blanket over your head and force yourself to breathe."

    "The knocking continues for exactly seven more minutes. You count."

    "Then silence. Just the sound of your own heartbeat, too loud in the dark."

    jump wrongness_pendant

label wrongness_record:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0

    "Your hands shake as you pull out your phone. Press record."

    "The knocking fills the tiny speaker—rhythmic, persistent, almost like..."

    "You play it back the next morning, in daylight, with coffee."

    "The knocking sounds almost like a pattern. Like morse code."

    "You look up the translation. It doesn't make sense: COME DOWN COME DOWN COME DOWN."

    "You delete the recording. Your hands are shaking again."

    jump wrongness_pendant

label wrongness_pendant:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_bedroom_day with dissolve

    "A few days later, you notice something wrong in Morgan's room."

    "The pendant—you kept it after she disappeared, couldn't bring yourself to throw it away—was in the nightstand drawer. Locked. You're certain."

    "Now it's on top of the nightstand. Facing the door. As if it's been waiting for you."

    menu:
        "Throw it away.":
            jump pendant_throw
        "Put it back in the drawer and lock it again.":
            jump pendant_lock
        "Wear it. Feel closer to Morgan.":
            jump pendant_wear
        "Research the symbol.":
            jump pendant_research

label pendant_throw:
    scene bg_trash with dissolve

    "You throw it in the trash. Take the bag out to the curb for good measure."

    "Some things need to be gone."

    scene bg_bedroom_day with fade

    "The next morning, it's on your pillow. Circle and line, warm against the fabric, as if it had never left."

    jump wrongness_tapestry

label pendant_lock:
    "You put it back. Lock the drawer. Check the lock twice. Three times."

    "It stays there for two days."

    scene bg_bedroom_day with fade

    "On the third morning, it's on your bathroom sink. Waiting."

    jump wrongness_tapestry

label pendant_wear:
    scene bg_mirror with dissolve

    "You slip the cord over your head. The pendant settles against your chest, warm despite the cold room."

    "For a moment, you feel something—a connection. A presence. Morgan, maybe. Or something wearing her memory like a coat."

    "The warmth spreads through you. It feels like understanding. It feels like coming home."

    jump wrongness_tapestry

label pendant_research:
    scene bg_computer with dissolve

    "You spend hours searching."

    "The symbol predates the Threshold Assembly by centuries. It appears in occult texts, alchemical manuscripts, scattered references across a dozen dead religions."

    "Always the same meaning: the threshold between above and below. The crossing point. The door that opens both ways."

    "One text calls it \"the mark of those who go down and do not return as themselves.\""

    "You close the laptop. The pendant sits on the desk beside you, somehow warmer than before."

    jump wrongness_tapestry

label wrongness_tapestry:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0
    scene bg_hallway_tapestry with dissolve

    "Days pass. The wrongness accumulates like dust. Sounds in the walls. Objects that move when you're not looking. Dreams of spiraling tunnels and something waiting at the bottom."

    "Then the water heater breaks. Of course it does."

    "You're doing laundry when you notice the tapestry moving. Billowing slightly, like there's a draft behind it."

    "Warm air seeps around its edges. The kind of warmth that shouldn't exist in a hallway. The kind Morgan told you to follow."

    menu:
        "Tear down the tapestry immediately.":
            jump discovery_tear_down
        "Look behind it carefully.":
            jump discovery_careful
        "Leave it. You're not ready.":
            jump discovery_not_ready

label discovery_tear_down:
    scene bg_hidden_door with dissolve

    "You grab the fabric and pull. It comes down in a heap of dust and fibers."

    "Behind it, where the water heater closet should be, is something else entirely."

    "A seam in the wall. A door that shouldn't exist."

    "It's slightly ajar. Warm, stale air seeps through the crack. You hear something—maybe just air moving. Maybe breathing."

    menu:
        "Open the door.":
            jump discovery_open
        "Call Detective Marsh first.":
            jump discovery_call_marsh
        "Get a weapon first.":
            jump discovery_weapon

label discovery_careful:
    scene bg_hidden_door with dissolve

    "You lift the edge of the tapestry. Slowly. Carefully."

    "The warm air hits your face immediately—thick, humid, smelling of earth and something else. Something organic."

    "Behind the tapestry is not the water heater closet. It's a door. A door that shouldn't exist, set into a wall that should be solid."

    "It's slightly ajar. Darkness beyond. Breathing darkness."

    menu:
        "Open the door.":
            jump discovery_open
        "Call Detective Marsh first.":
            jump discovery_call_marsh
        "Get a weapon first.":
            jump discovery_weapon

label discovery_not_ready:
    "You turn away. Go back downstairs. Pour yourself a drink."

    "Try to forget the warmth, the movement, the sense of something waiting just behind the fabric."

    "You're not ready. You may never be ready."

    scene bg_hallway_tapestry with fade

    "That night, you wake standing in the upstairs hallway."

    "The tapestry is on the floor. The door is open."

    "You don't remember getting out of bed. You don't remember pulling down the tapestry."

    "But here you are. Standing at the threshold. Warm air breathing against your face."

    menu:
        "Open the door.":
            jump discovery_open
        "Call Detective Marsh first.":
            jump discovery_call_marsh
        "Get a weapon first.":
            jump discovery_weapon

label discovery_open:
    play music "audio/music/descent.wav" fadeout 1.0 fadein 1.0
    scene bg_spiral_stairs with dissolve

    "You push the door open."

    "Beyond it is not a closet. Not a water heater."

    "It's a narrow passage. And a staircase—spiraling down into darkness."

    "The stairs are carved from stone, worn smooth by countless feet. They look ancient. Far older than the house. Far older than anything should be."

    "Warm air rises from below, carrying the scent of earth and time and something alive."

    menu:
        "Descend immediately.":
            jump level1_antechamber
        "Go back. Prepare. Return tomorrow.":
            jump discovery_prepare
        "Seal the door and try to forget.":
            jump discovery_seal

label discovery_call_marsh:
    play music "audio/music/tension.wav" fadeout 1.0 fadein 1.0

    "You call Marsh. Tell him what you found. He's skeptical but agrees to come look."

    "When he arrives, the door is gone. Just a wall. Just a water heater closet."

    "\"Grief does strange things,\" he says gently."

    "You stand in the hallway after he leaves, hand pressed against solid wall. Knowing what you saw. Knowing what's behind it."

    scene bg_hidden_door with fade

    "That night, the door reappears. This time, you don't hesitate."

    jump discovery_open

label discovery_weapon:
    play music "audio/music/tension.wav" fadeout 1.0 fadein 1.0

    "You find a kitchen knife. Heavy. Real. Something solid to hold onto."

    "Then you return to the door. It's still there. Still waiting. Still breathing warm air into the hallway."

    "The knife feels useless somehow. Whatever is down there, you sense it can't be hurt by something so small."

    "But you hold it anyway. It's the only armor you have."

    jump level1_antechamber

label discovery_prepare:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_bedroom_dark with dissolve

    "You step back. Close the door—but not all the way. Tomorrow. Tomorrow you'll be ready."

    "You gather supplies: flashlight, phone, water bottle. Sensible things. Human things."

    "You try to sleep. Dream of Morgan's face, smiling in the dark."

    "\"You came,\" she says. \"I knew you would.\""

    "You wake at 3:17 AM. You're already walking toward the stairs."

    jump level1_antechamber

label discovery_seal:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_hallway_sealed with dissolve

    "You slam the door. Nail boards across it. Push a dresser in front."

    "This is insane. This is impossible. Doors don't appear in walls. Staircases don't exist under houses."

    "You're losing your mind with grief, that's all."

    scene bg_spiral_stairs with fade

    "That night, you wake standing at the door."

    "The dresser is back against the wall. The boards are neatly stacked in the corner. The door is open."

    "And your feet are on the first step, already descending, before your mind catches up."

    jump level1_antechamber

# ============================================
# ACT IV - THE DESCENT
# ============================================

label level1_antechamber:
    play music "audio/music/descent.wav" fadeout 1.0 fadein 1.0
    scene bg_antechamber with fade

    "The stone stairs spiral down for what feels like hours."

    "The walls are covered in symbols—the same symbol from the pendant, repeated hundreds of times. Some carved. Some drawn in something dark and flaking."

    "Finally, the stairs open into a chamber. Stone walls. Dirt floor. And signs of habitation."

    "Sleeping bags. Empty water bottles. Journals scattered across the ground."

    "This was a meeting place. A gathering point. Someone—many someones—were here before you."

    menu:
        "Read the journals.":
            jump level1_journals
        "Search for another exit.":
            jump level1_search
        "Call out. See if anyone responds.":
            jump level1_call

label level1_journals:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "The journals are disturbing. Entries from dozens of different hands. Different names. Different stories."

    "All talking about \"the descent.\" About \"shedding the body's failure.\" About \"becoming.\""

    "The entries get stranger as you read. Fever-bright descriptions of visions. Promises of transcendence."

    "And then, over and over, the same final words: \"I'M READY.\""

    "After that, the pages are blank. As if the writers simply ceased to exist."

    jump level1_morgan_journal

label level1_search:
    "You circle the chamber, running your hands along the walls. Stone. Solid. Ancient."

    "But there—in the far corner—a tunnel. Narrow, barely wide enough for one person, sloping further down into darkness."

    "The warm air flows from this tunnel. And something else. A faint sound, like distant humming. A melody you almost recognize."

    "But first, you notice the journals scattered on the ground. Morgan's handwriting catches your eye."

    jump level1_morgan_journal

label level1_call:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0

    "\"Hello?\" Your voice echoes. Bounces off stone walls and returns to you, distorted. Hollow."

    "No answer. Just the echo dying slowly, and then—so faint you might have imagined it—something that sounds like your name."

    "Called from very far below."

    "You don't call out again. Instead, your eyes fall on the journals scattered across the ground. One of them has Morgan's handwriting on the cover."

    jump level1_morgan_journal

label level1_morgan_journal:
    play music "audio/music/grief.wav" fadeout 1.0 fadein 1.0

    "You find Morgan's journal. Her handwriting fills the pages—cramped, urgent, increasingly unhinged."

    "The last entry reads: \"They're wrong about one thing. It's not about dying. It's about going deeper. The lowest point is where you become. I'm not afraid. I was never afraid. I was just waiting to understand.\""

    "The page after that is blank. But on the back cover, in tiny letters: \"Follow me down.\""

    menu:
        "Take the journal with you.":
            jump level2_residences
        "Leave it. You don't want it.":
            jump level2_residences
        "Read more entries, looking for clues.":
            jump level1_more_entries

label level1_more_entries:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "You read more. Hours pass, maybe—it's hard to tell down here."

    "The entries paint a picture: the Threshold Assembly found people like Morgan. Sick. Desperate. Searching for meaning in their pain."

    "They offered answers. Showed them the tunnels beneath their own homes. Doors that \"opened from inside.\""

    "And one by one, the faithful went down. Descending toward something that waited. Something that wanted."

    "None of them came back up. At least, not as themselves."

    jump level2_residences

label level2_residences:
    play music "audio/music/descent.wav" fadeout 1.0 fadein 1.0
    scene bg_residences with fade

    "The tunnel slopes further down. The air grows thicker, warmer."

    "And then it opens into something impossible."

    "A neighborhood carved from stone. Alcoves in the walls, dozens of them, each one a small living space. Beds. Personal effects. Photos pinned to rough walls."

    "Someone lived here. Many someones."

    "It looks like it was abandoned recently. Or maybe not abandoned at all."

    "One of the alcoves has a lantern still burning. The bed is unmade."

    menu:
        "Wait and watch.":
            jump level2_wait
        "Search the alcove.":
            jump level2_search_alcove
        "Call out.":
            jump level2_call
        "Move past quickly.":
            jump level2_photos

label level2_wait:
    play music "audio/music/tension.wav" fadeout 1.0 fadein 1.0

    "You press yourself against the wall. Wait. Listen."

    "For a long time, nothing. Just the flicker of the lantern. The thick silence of deep earth."

    "Then—shuffling. Movement. Something deeper in the tunnel, moving away from you. Not toward."

    "You catch a glimpse of fabric. A robe, maybe."

    "Whoever or whatever it was, it didn't see you. Or didn't care."

    "You move to the wall of photographs."

    jump level2_photos

label level2_search_alcove:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_alcove with dissolve

    "The alcove is small but lived-in. Blankets on the bed, still warm. A cup of water, recently filled."

    "And on the small stone shelf, a notebook open to a half-written entry: \"They said the new one would come soon. The one from above. We've been waiting—\""

    "The entry stops mid-sentence. As if the writer was interrupted. Or called away."

    "On the wall, photographs."

    jump level2_photos

label level2_call:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0

    "\"Hello?\" The word echoes strangely. Doesn't come back right. Almost sounds like a different voice returning it."

    "No one answers. But you hear movement—shuffling footsteps retreating deeper into the tunnel."

    "They heard you. They chose not to respond."

    "The photographs on the wall draw your attention."

    jump level2_photos

label level2_photos:
    play music "audio/music/grief.wav" fadeout 1.0 fadein 1.0
    scene bg_photos with dissolve

    "The photographs cover one wall. Dozens of them. People in robes, standing together. Smiling."

    "Their faces are calm, peaceful, emptied of fear."

    "And there—in the center of one photo—is Morgan."

    "Standing with the others. Smiling that same empty smile."

    "Behind the group, a massive dark opening. A pit, yawning wide."

    "Morgan's hand is raised, pointing toward it. Inviting you to follow."

    menu:
        "Take the photograph.":
            jump level3_cathedral
        "Look for other faces you recognize.":
            jump level2_recognize
        "Keep moving. You need to find Morgan.":
            jump level3_cathedral

label level2_recognize:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0

    "You scan the faces. Most are strangers."

    "But one—the person from the funeral. The one who gave you the envelope."

    "They're standing next to Morgan, hand on her shoulder."

    "In the photo, they're smiling. Looking directly at the camera. Looking directly at you."

    "Like they knew you'd be here. Like they've been waiting."

    jump level3_cathedral

label level3_cathedral:
    play music "audio/music/awe.wav" fadeout 1.0 fadein 1.0
    scene bg_cathedral with fade

    "The tunnel opens into a cavern so vast your flashlight can't reach the ceiling."

    "It swallows sound, swallows light, swallows everything but the sense of ancient, patient presence."

    "In the center: an altar of dark stone."

    "Around it, thousands of candles burned down to nothing. Rivers of hardened wax frozen on the floor like geological formations."

    "On the altar sits a book. Handwritten. Bound in something you don't want to identify."

    "The title page reads: \"THE RITES OF THRESHOLD.\""

    menu:
        "Read the book.":
            jump level3_read_book
        "Destroy it.":
            jump level3_destroy_book
        "Leave it and continue deeper.":
            jump level3_pit

label level3_read_book:
    play music "audio/music/dread.wav" fadeout 1.0 fadein 1.0
    scene bg_ritual_book with dissolve

    "The book describes a ritual. A \"willing descent.\" The faithful go down, and down, and down, until they reach \"the lowest place.\""

    "There, they \"shed the body's failure\" and \"become one with what waits.\""

    "The language is reverent, ecstatic. It speaks of transcendence. Of freedom from pain, from illness, from the prison of flesh."

    "It speaks of becoming something larger. Something eternal. Something that was here before the house, before the tunnels, before anything at all."

    scene bg_pit with dissolve

    "Behind the altar, a pit yawns in the floor. The warm air rises from it. The ladder rungs are worn smooth by countless hands."

    jump level3_pit

label level3_destroy_book:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0

    "You grab the book. Tear the pages. But they won't tear right—they flex like skin, resist like muscle."

    "And when you try to throw it into the pit, your arm won't move."

    "Something holds you. Not a hand. Not a force. Just a certainty, deep in your bones, that destroying this would be wrong."

    "That this book is older than wrong and right. That it simply is."

    "You set it back on the altar. Your hands are shaking."

    scene bg_pit with dissolve

    "Behind the altar, the pit waits."

    jump level3_pit

label level3_pit:
    play music "audio/music/descent.wav" fadeout 1.0 fadein 1.0
    scene bg_pit with dissolve

    "Behind the altar, a hole in the floor. A pit descending into absolute darkness."

    "The warm air rises from it, thick and living."

    "You can see the first rungs of a ladder, ancient iron set into stone, leading down into nothing."

    "This is it. The lowest place. Where Morgan went. Where they all went."

    menu:
        "Climb down.":
            jump level4_warren
        "Drop something and listen for it to hit bottom.":
            jump level3_drop
        "Call Morgan's name into the pit.":
            jump level3_call_morgan

label level3_drop:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0

    "You find a loose stone. Drop it into the darkness."

    "Count the seconds."

    "One. Two. Three. Four. Five..."

    "Ten..."

    "Twenty..."

    "There is no sound. Either the pit is bottomless, or whatever's down there absorbed the impact. Or the stone never landed at all."

    "The ladder rungs wait."

    jump level4_warren

label level3_call_morgan:
    play music "audio/music/horror.wav" fadeout 1.0 fadein 1.0

    "\"Morgan?\""

    "The name falls into the pit. Swallowed by darkness."

    "Silence."

    "Then, from very far below—so far it shouldn't be possible to hear anything—something that might be an echo."

    "Or might be a response."

    "Your name. Spoken in Morgan's voice. Warm and welcoming and utterly wrong."

    jump level4_warren

label level4_warren:
    play music "audio/music/descent.wav" fadeout 1.0 fadein 1.0
    scene bg_warren with fade

    "The ladder goes down for a long time. Your arms ache. Your hands cramp on the ancient rungs."

    "The walls close in—this is a shaft now, barely wide enough for one person, stone pressing against your shoulders."

    "You emerge into a warren of tunnels. They branch in every direction, identical and endless."

    "The walls are wet. The air is thick and warm."

    "You could wander here forever and never find your way out. Unless you're careful. Unless you're smart. Unless you know how to navigate."

    menu:
        "Mark your path as you go—tear cloth, scratch walls.":
            jump level4_mark
        "Follow the warmest air current.":
            jump level4_warmth
        "Follow the faint sound you keep almost hearing.":
            jump level4_sound
        "Trust your instincts and move randomly.":
            jump level4_instinct

label level4_mark:
    "You tear strips from your shirt. Leave them at each turn. Scratch arrows into the wet stone."

    "If nothing else, you'll be able to find your way back. If there is a back. If there's anything left to go back to."

    "The tunnels twist and branch and merge. But eventually, following the marks, correcting your course, you find yourself moving in one direction."

    "Deeper. Toward something that feels like an ending."

    jump reunion_approach

label level4_warmth:
    "Follow the warm air. Morgan's words echo in your memory."

    "You hold your hand out at each junction, feeling for the current."

    "There—stronger on the left. And again—the right path is warmer."

    "The warmth leads you deeper. Always deeper. Like a breath drawing you in. Like a pulse pulling you toward its source."

    jump reunion_approach

label level4_sound:
    play music "audio/music/grief.wav" fadeout 1.0 fadein 1.0

    "There—that sound again. Humming. A melody, distant and distorted, rising from the tunnels ahead."

    "You know that tune. Morgan used to hum it when she was tired. When she was falling asleep."

    "You follow it through the maze, and it leads you true."

    "The humming grows clearer. Closer. Until you can almost make out words. Almost recognize the voice."

    jump reunion_approach

label level4_instinct:
    "You stop thinking. Stop planning. Let your feet carry you where they will."

    "Left, right, straight, back. The tunnels blur together. Time loses meaning."

    "And somehow, impossibly, you find yourself moving forward. As if the maze wants you to reach its center."

    "As if you were always meant to arrive here."

    "As if this was never really a choice at all."

    jump reunion_approach

# ============================================
# ACT V - THE REUNION
# ============================================

label reunion_approach:
    play music "audio/music/finale.wav" fadeout 1.0 fadein 1.0
    scene bg_lowest_place with fade

    "You emerge into a chamber. The final chamber. The lowest place."

    "The floor is soft—not stone. Something organic. Yielding under your feet like flesh."

    "The warmth is oppressive, tropical, wrong."

    "And in the center of the room, sitting with their back to you, is a figure."

    "They're wearing Morgan's clothes. Sitting perfectly still. Waiting."

    menu:
        "Say their name.":
            jump reunion_name
        "Approach silently.":
            jump reunion_silent
        "Stay at the entrance. Don't go closer.":
            jump reunion_stay

label reunion_name:
    "\"Morgan?\""

    "The figure stiffens. Then, slowly, turns."

    "It's Morgan—but wrong. Their face is theirs, but the proportions have shifted subtly. Eyes too calm. Smile too wide. They don't seem to breathe."

    "\"You came.\" Their voice is Morgan's voice, but layered somehow. Echoed by something beneath it. \"I wasn't sure you would.\""

    jump reunion_conversation

label reunion_silent:
    "You move closer, silent on the soft floor. The figure doesn't move. Doesn't acknowledge you."

    "Until you're almost close enough to touch, and then—without turning—they speak."

    "\"You came.\" Morgan's voice. Morgan's words. But somehow not Morgan at all. \"I felt you descending. I felt you the whole way down.\""

    "They turn. Their face is Morgan's, but shifted. Changed. Perfected in a way that feels deeply wrong."

    jump reunion_conversation

label reunion_stay:
    "You freeze at the threshold. Something tells you not to go closer. Not to step onto that soft, yielding floor."

    "The figure stands. Turns. Morgan's face—but not. The proportions wrong. The smile too wide. The eyes too empty of the fear that always lived there before."

    "\"You came.\" They take a step toward you. The floor pulses under their feet. \"I knew you would. Eventually. Everyone finds their way down, eventually.\""

    jump reunion_conversation

label reunion_conversation:
    "\"Morgan...\" You don't know what to say. What can you say? They're here. They're alive. They're something else entirely."

    menu:
        "\"What happened to you?\"":
            jump reunion_what_happened
        "\"I'm here to take you home.\"":
            jump reunion_take_home
        "\"What is this place?\"":
            jump reunion_what_place
        "\"Are you... alive?\"":
            jump reunion_alive

label reunion_what_happened:
    "\"I became.\" Morgan smiles that too-wide smile. \"The illness was always going to take me. The Assembly showed me another way. I went down, and down, and down. And at the bottom, I found something that wanted me.\""

    "They spread their arms, indicating the chamber, the darkness, the something you can feel watching from everywhere at once."

    "\"I'm not sick anymore. I'm not dying. I'm not even really me anymore. But I remember you. I still love you.\""

    "They extend a hand."

    "\"You could stay. You don't have to be afraid. You don't have to be alone.\""

    jump final_choice

label reunion_take_home:
    "Morgan laughs. It's almost a human sound. Almost."

    "\"Home? This is home now. More than that house ever was.\""

    "They step closer. You can smell them now—earth and something sweeter, something organic and alive."

    "\"The illness was going to take everything. The pain, the exhaustion, the slow vanishing of who I used to be. This was better. This is better.\""

    "They reach for your hand. Their skin is cold but somehow also warm. Wrong temperature. Impossible temperature."

    "\"You could stay. With me. Forever.\""

    jump final_choice

label reunion_what_place:
    "\"The lowest place.\" Morgan's voice echoes strangely, as if the chamber itself is speaking through them. \"Where the threshold meets what waits. What has always waited.\""

    "The darkness around you seems to pulse. Breathe."

    "\"It was here before the house. Before the land. Before anything at all. It doesn't want. It doesn't need. It just... is. And anyone who descends far enough becomes part of its isness.\""

    "They extend a hand."

    "\"You could understand. If you stayed.\""

    jump final_choice

label reunion_alive:
    "\"Alive?\" Morgan tilts their head, considering. \"That's a surface word. Up there, you're alive or you're dead. Down here...\""

    "They gesture at the pulsing darkness."

    "\"Down here, there are other options.\""

    "They step closer. You can see now—they don't breathe. Their chest doesn't move. But something in them lives. Something that wears Morgan's face like a comfortable memory."

    "\"I'm not afraid anymore. Not in pain. Not waiting to die.\""

    "They extend a hand."

    "\"You don't have to be either.\""

    jump final_choice

label final_choice:
    "Morgan's hand hangs in the air between you. Cold fingers extended."

    "Behind them, the darkness pulses. Watches. Waits."

    "You can feel it—the thing beneath everything. Ancient and patient. Hungry in a way that has nothing to do with appetite."

    "The way back is still open. For now. You can feel the ladder behind you, the tunnels, the spiral stairs rising toward light and air and the world you used to know."

    "This is the choice. The only choice that ever mattered."

    menu:
        "Take their hand. Stay. Become.":
            jump ending_a
        "Refuse and flee. Run. Don't look back.":
            jump ending_b
        "Try to pull them out by force.":
            jump ending_c
        "\"Show me. Help me understand.\"":
            jump ending_d

# ============================================
# ENDINGS
# ============================================

label ending_a:
    $ persistent.endings_seen.add("communion")

    play music "audio/music/ending_a.wav" fadeout 1.0 fadein 1.0
    scene bg_communion with fade

    "You take their hand. It's cold, then warm, then something beyond temperature. Beyond sensation."

    "Morgan smiles—really smiles—and pulls you forward, into the darkness, into the warmth, into the vast and patient presence that waits beneath everything."

    "You descend. Together this time."

    "The fear dissolves. The grief dissolves. Your sense of self begins to blur at the edges, to merge with something larger."

    "You understand now. It's not death. It's not life. It's becoming."

    scene black with fade
    pause 1.0

    "Above, in the house that was once yours, the door seals itself. The tapestry falls back into place."

    "Eventually, the house is sold. A young couple moves in. They seem happy."

    "The real estate agent mentions there's a bit of draft in the upstairs hallway—probably just needs weather-stripping. Nothing to worry about."

    "They'll get used to it. Everyone does, eventually."

    "Everyone finds their way down."

    scene black with fade
    centered "{size=+10}ENDING: COMMUNION{/size}"
    pause 2.0

    return

label ending_b:
    $ persistent.endings_seen.add("escape")

    play music "audio/music/ending_b.wav" fadeout 1.0 fadein 1.0
    scene bg_escape with fade

    "\"No.\" You step back. Turn. Run."

    "Behind you, Morgan doesn't chase. Doesn't call out. Just watches with those too-calm eyes as you scramble toward the ladder, the tunnels, the spiral stairs."

    "The warren shifts around you, but you marked your path. Left here. Right there. Following the arrows scratched in stone, the torn fabric hanging from the walls."

    "The climb is endless. Your arms burn. Your lungs scream."

    "But finally—finally—you emerge into your own hallway, gasping, covered in dust and sweat and something darker."

    scene black with dissolve

    "You seal the door. Nail it shut. Push the heaviest furniture you own against it."

    "Then you sell the house. Take the first offer. Never look back."

    "You move across the country. Start over. Try to forget."

    "Mostly, you succeed."

    "But some nights, you wake at 3:17 AM to the feeling of warm breath on the back of your neck."

    "And you know—you will always know—that the door is still there. Waiting. In case you ever change your mind."

    scene black with fade
    centered "{size=+10}ENDING: ESCAPE{/size}"
    pause 2.0

    return

label ending_c:
    $ persistent.endings_seen.add("defiance")

    play music "audio/music/ending_c.wav" fadeout 1.0 fadein 1.0
    scene bg_defiance with fade

    "You grab Morgan's hand—not to stay, but to pull."

    "\"We're leaving. Now.\""

    "Morgan doesn't fight. Doesn't resist. Just looks at you with infinite sadness."

    "\"You can't save me. I'm not lost.\""

    "You pull harder. Drag them toward the ladder."

    # Screen shake for horror effect
    show screen shake

    "And then the darkness moves."

    "Not a metaphor. Not a feeling. The chamber itself contracts. The floor ripples. Something vast and ancient and utterly indifferent notices you for the first time."

    "You are very, very small."

    "\"Go,\" Morgan whispers. \"While it still lets you.\""

    hide screen shake

    scene black with dissolve

    "You run. Somehow, impossibly, you make it. The tunnels release you. The stairs spit you out into your own hallway, alone, shaking, alive."

    "The door seals itself behind you with a sound like a sigh."

    "Morgan is gone. Really gone now."

    "But when you look at your palm, there's a mark. Circle and line. The threshold symbol, burned into your skin like a brand."

    "A reminder. A promise. A door that can never fully close."

    scene black with fade
    centered "{size=+10}ENDING: DEFIANCE{/size}"
    pause 2.0

    return

label ending_d:
    $ persistent.endings_seen.add("understanding")

    play music "audio/music/ending_d.wav" fadeout 1.0 fadein 1.0
    scene bg_understanding with fade

    "\"Show me.\""

    "Morgan takes your hand—but doesn't pull. Their cold fingers interlock with yours, and suddenly you're not in the chamber anymore."

    "You're everywhere. Nowhere."

    scene black with dissolve

    "You see the thing beneath—vast and patient, older than geology, older than time."

    "You see the faithful, absorbed into its vastness. Not dead. Not alive. Part of something. Threads in an infinite tapestry, woven into the fabric of what waits beneath everything."

    "You see Morgan among them. Content. Connected. Free of pain, free of fear, free of the slow betrayal of a body that was always failing them."

    "You understand. Not everything—no human mind could hold everything—but enough."

    "Enough to know that this isn't evil. Isn't good. It simply is. Has always been. Will always be."

    scene bg_spiral_stairs with fade

    "You wake at the base of the ladder. Alone. The chamber is empty. Morgan is gone."

    "The tunnels behind you have collapsed. There's only one way now: up."

    "You climb. Emerge into your hallway. The door is gone. Just a wall. Just a water heater closet."

    "Was any of it real?"

    "You touch your chest. The pendant hangs there—Morgan's pendant—warm against your skin. You don't remember putting it on."

    "But you know, now. You understand. And you will carry that understanding for the rest of your life."

    "A door that opened inward. A truth you can never unknow."

    scene black with fade
    centered "{size=+10}ENDING: UNDERSTANDING{/size}"
    pause 2.0

    return

# Shake screen definition
screen shake:
    add Solid("#000") at shake
