m = {{'arisu', 'koharu', 'yoshino', 'yukimi', 'yumi'},
{'arisu', 'koharu', 'yukimi', 'yoshino', 'yumi'},
{'arisu', 'koharu', 'yumi', 'yoshino', 'yukimi'},
{'arisu', 'yoshino', 'koharu', 'yukimi', 'yumi'}, 
{'arisu', 'yoshino', 'yukimi', 'koharu', 'yumi'}, 
{'arisu', 'yoshino', 'yumi', 'koharu', 'yukimi'}, 
{'arisu', 'yukimi', 'koharu', 'yoshino', 'yumi'},
{'arisu', 'yukimi', 'yoshino', 'koharu', 'yumi'}, 
{'arisu', 'yukimi', 'yumi', 'koharu', 'yoshino'}, 
{'arisu', 'yumi', 'koharu', 'yoshino', 'yukimi'}, 
{'arisu', 'yumi', 'yoshino', 'koharu', 'yukimi'}, 
{'arisu', 'yumi', 'yukimi', 'koharu', 'yoshino'}, 
{'koharu', 'arisu', 'yoshino', 'yukimi', 'yumi'}, 
{'koharu', 'arisu', 'yukimi', 'yoshino', 'yumi'}, 
{'koharu', 'arisu', 'yumi', 'yoshino', 'yukimi'}, 
{'koharu', 'yoshino', 'arisu', 'yukimi', 'yumi'}, 
{'koharu', 'yukimi', 'arisu', 'yoshino', 'yumi'}, 
{'koharu', 'yumi', 'arisu', 'yoshino', 'yukimi'},
{'yoshino', 'arisu', 'koharu', 'yukimi', 'yumi'}, 
{'yoshino', 'koharu', 'arisu', 'yukimi', 'yumi'}};

colortable = {
	'6248317119581156241581539894516772778',
'62483171195811551362851005422516772778',
'62483171195811515124625100542254014977',
'6248317972398212813157539894516772778',
'6248317972398251362851353996616772778',
'6248317972398215124625135399664014977',
'62483177239106128131571005422516772778',
'6248317723910662415811353996616772778',
'62483177239106151246251353996612485217',
'62483171239761812813157100542254014977',
'6248317123976186241581135399664014977',
'62483171239761851362851353996612485217',
'1664021065783086241581539894516772778',
'16640210657830851362851005422516772778',
'16640210657830815124625100542254014977',
'1664021097239827236250539894516772778',
'16640210723910672362501005422516772778',
'16640210123976187236250100542254014977',
'10053459657830812813157539894516772778',
'10053459119581157236250539894516772778'
}
-- pre-defined functions 
function endless_vibrate()
	while 1 do 
	vibrate()
	usleep(1000000)
	end
end 

function down() 
touchDown(5, 909.60, 854.12);
usleep(84566.29);
touchUp(5, 909.60, 854.12);
end

function kettei() 
touchDown(2, 1843.36, 1027.13);
usleep(66662.83);
touchUp(2, 1843.36, 1027.13);
end

function start() 
touchDown(2, 1844.30, 1027.13);
usleep(98609.79);
touchUp(2, 1844.30, 1027.13);
end

function assistive() 
touchDown(4, 78.20, 655.02);
usleep(49974.29);
touchUp(4, 78.20, 655.02);
end

function controlpanel() 
touchDown(1, 1388.56, 772.93);
usleep(15095.29);
touchUp(1, 1388.56, 772.93);
end

function record() 
touchDown(3, 2155.24, 546.77);
usleep(116574.54);
touchUp(3, 2155.24, 546.77);
end

function home() 
keyDown(KEY_TYPE.HOME_BUTTON);
usleep(140158.67);
keyUp(KEY_TYPE.HOME_BUTTON);
end

function onoff() 
touchDown(5, 2025.86, 302.24);
usleep(101521.12);
touchUp(5, 2025.86, 302.24);
end

function wait(time)
usleep(time * 1000000)
end

function down() 
touchDown(5, 909.60, 854.12);
usleep(84566.29);
touchUp(5, 909.60, 854.12);
end

function kettei() 
touchDown(2, 1843.36, 1027.13);
usleep(66662.83);
touchUp(2, 1843.36, 1027.13);
end

function triple_home() 
keyDown(KEY_TYPE.HOME_BUTTON);
usleep(100088.00);
keyUp(KEY_TYPE.HOME_BUTTON);
usleep(60051.00);

keyDown(KEY_TYPE.HOME_BUTTON);
usleep(80075.00);
keyUp(KEY_TYPE.HOME_BUTTON);
usleep(60093.00);

keyDown(KEY_TYPE.HOME_BUTTON);
usleep(60012.00);
keyUp(KEY_TYPE.HOME_BUTTON);
end

function open_swap_palette()
	touchDown(5, 502.10, 610.56);
	usleep(83144.46);
	touchUp(5, 502.10, 610.56);
	usleep(2151893.88);

	touchDown(6, 634.41, 303.20);
	usleep(48388.50);
	touchUp(6, 634.41, 303.20);

end

function close_swap_palette()
touchDown(1, 97.50, 86.70);
usleep(66430.71);
touchUp(1, 97.50, 86.70);
end

function swap(i,j)
    swap_dict = {
		{611.23, 280.01},
		{859.40, 292.57},
		{1128.80, 338.97},
		{1329.63, 298.37},
		{1563.31, 321.57}
	}
	touchDown(2, swap_dict[i][1], swap_dict[i][2]);
	usleep(81898.79);
	touchUp(2, swap_dict[i][1], swap_dict[i][2]);
	usleep(701670.50);

	usleep(2000000)
	
	touchDown(3, swap_dict[j][1], swap_dict[j][2]);
	usleep(81898.79);
	touchUp(3, swap_dict[j][1], swap_dict[j][2]);
	usleep(701670.50);
	
	usleep(2000000)
	
	-- close confirmation dialog
	touchDown(4, 1307.43, 1058.06);
	usleep(84972.58);
	touchUp(4, 1307.43, 1058.06);
	usleep(1000000)	
end

function assemble_idols(i)
	open_swap_palette()
	usleep(1000000)
    -- assemble the i+1th composition in matrix m 
    -- make copy of arrays of interst
    old_comp = m[i]
    new_comp = m[i+1]
    for j = 1,4 do
        if new_comp[j] ~= old_comp[j] then
            for k = 1,5 do
                if old_comp[k] == new_comp[j] then
                    swap(k,j)
					temp_storage = old_comp[k]
					old_comp[k] = old_comp[j]
					old_comp[j] = temp_storage
                end
            end
        end
    end
	usleep(w)
	close_swap_palette()
end

function assemble_costumes(i)
	usleep(1e6)
	costume_coord = {
		{513.69, 857.02},
		{842.02, 814.49},
		{1143.28, 808.69},
		{1396.27, 818.36},
		{1717.82, 796.13}
		}

	
	for j = 1,5 do
		-- set koharu's costume
		if m[i][j] == 'koharu' then
			-- click costume icon belonging to koharu
			touchDown(2, costume_coord[j][1], costume_coord[j][2]);
			usleep(64972.58);
			touchUp(2, costume_coord[j][1], costume_coord[j][2]);

			usleep(2000000)

			-- swap Koharu's costume to CD 
			touchUp(1, 1956.33, 568.03);
			usleep(220998.21);

			-- updated koharu costume 
			touchDown(2, 1942.81, 566.10);
			usleep(98202.62);
			touchUp(2, 1942.81, 566.10);
			usleep(1033806.04);

			touchDown(6, 1428.15, 372.79);
			usleep(99588.04);
			touchUp(6, 1428.15, 372.79);
			usleep(1000000);

			touchDown(2, 1160.67, 1104.45);
			usleep(82967.92);
			touchUp(2, 1160.67, 1104.45);
			
		-- arisu costume
		elseif m[i][j] == 'arisu' then
			touchDown(2, costume_coord[j][1], costume_coord[j][2]);
			usleep(64972.58);
			touchUp(2, costume_coord[j][1], costume_coord[j][2]);

			usleep(2000000)
			for k = 1,5 do
				if m[i][k] == 'yukimi' then
					if j + k == 6 then -- if arisu and yukimi are symmetric make arisu SSB
						touchDown(3, 468.31, 689.81);
						usleep(83024.88);
						touchUp(3, 468.31, 689.81);
						usleep(785883.96);

						touchDown(4, 1175.16, 1109.28);
						usleep(64750.25);
						touchUp(4, 1175.16, 1109.28);
						
						usleep(1000000);
					elseif j + k ~= 6 then -- make her SSB regardless, in this variant of the script
						touchDown(3, 468.31, 689.81);
						usleep(83024.88);
						touchUp(3, 468.31, 689.81);
						usleep(785883.96);

						touchDown(4, 1175.16, 1109.28);
						usleep(64750.25);
						touchUp(4, 1175.16, 1109.28);
					end
				end
			end
		
		elseif m[i][j] == 'yukimi' then 
			touchDown(2, costume_coord[j][1], costume_coord[j][2]);
			usleep(64972.58);
			touchUp(2, costume_coord[j][1], costume_coord[j][2]);
			usleep(2000000)

			touchDown(3, 468.31, 689.81);
			usleep(83024.88);
			touchUp(3, 468.31, 689.81);
			usleep(785883.96);

			touchDown(4, 1175.16, 1109.28);
			usleep(64750.25);
			touchUp(4, 1175.16, 1109.28);
		end
		usleep(1000000)
	end
end


-- function to extract 5 colors from the screen 
function extract_five_colors()
	color1 = tostring(getColor(513,534))
	color2 = tostring(getColor(850,517))
	color3 = tostring(getColor(1130,527))
	color4 = tostring(getColor(1435,523))
	color5 = tostring(getColor(1687,508))
	colorsum = color1 .. color2 .. color3 .. color4 .. color5
	return colorsum
end

-- function that takes as input a table containing int values representing 5 colors, and converts them into names
function get_index_from_colorsum(colorsum)
	for i = 1,60 do 
		if colortable[i] == colorsum then
			return i 
		end
	end
	return 0 
end

-- function to make sure composition is correct
function assert_correct_composition(i)
	
	if colortable[i] ~= extract_five_colors() then
		endless_vibrate()
	end
end

--check color to get initial starting point 
wait(3);
colorsum = extract_five_colors()
CURRENT = get_index_from_colorsum(colorsum)

--run script as usual, add a check for expected idol composition on screen 
i = CURRENT
w = 3

if i == 1 then -- initial, if first recording
	assemble_costumes(i);
	wait(w);
	triple_home();
	wait(w+1);
	assistive();
	wait(w-1);
	controlpanel();
	wait(w-1);
	record();
	wait(w-1)
	home();
	wait(w);
	triple_home();
	wait(w);
	start();
	for j = 1,33 do
	  wait(5);
	end
	triple_home();
	wait(w+1)
	assistive();
	wait(w-1);
	controlpanel();
	wait(w-1);
	record();
	wait(w-1)
	home();
	wait(w);
	triple_home();
	wait(10)
	kettei()
	wait(8)
end


while i ~= 20 do -- main loop
	assemble_idols(i)
	i = i + 1
	wait(w)
	assert_correct_composition(i)
	wait(w)
	assemble_costumes(i)
	wait(w-1);
	triple_home();
	wait(w)
	assistive();
	wait(w);
	controlpanel();
	wait(w-1);
	record();
	wait(w-1)
	home();
	wait(w);
	triple_home();
	wait(w);
	start();
	for j = 1,33 do
	  wait(5);
	end
	triple_home();
	wait(w+1)
	assistive();
	wait(w-1);
	controlpanel();
	wait(w-1);
	record();
	wait(w-1)
	home();
	wait(w);
	triple_home();
	wait(10)
	kettei()
	wait(8)
end