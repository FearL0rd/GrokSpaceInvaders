# Grok Space invaders

## Description

This is a GROK 3 code generation test.
The game will automatically detect your resolution, print it, and use half for the window size, scaling all elements.

## Getting Started

### Dependencies

* Python
* Pygame, pyautogui, screeninfo

### Installing

* install python components using pip install pygame pyautogui screeninfo
* download spaceinvaders.py

### Executing program

* How to run the program
* python spaceinvaders.py

## Notes

If the alien drop speed of 0.5 * scale_factor is too fast (e.g., aliens reach the bottom too quickly), try reducing enemy_drop_distance to a value like 0.25 * scale_factor or 0.3 * scale_factor for a moderate increase in speed, or 0.4 * scale_factor for something in between. For example:
0.25 * scale_factor: Slower but still quicker than 0.15.
0.3 * scale_factor: Moderately faster.
0.4 * scale_factor: Faster but less aggressive than 0.5.
If your resolution differs (e.g., 1920x1080, making half 960x540), the script will adjust automatically, but let me know if scaling feels off, and I can fine-tune.
The game retains all previous mechanics, including bullet passing, gradual bunker destruction, and other features.
If the bunker, aliens, or player need further boldness or visibility adjustments, let me know, and I can refine bunker_pixel_size, alien_pixel_size, or player_pattern.
If you see rendering issues, ensure Pygame is up-to-date (pip install --upgrade pygame).

## Authors

Contributors Fearl0rd and GROK3

## License

This project is licensed under the MIT License 
