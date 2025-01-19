##### This project was made as the final project for the course [CS50 of harvard](https://pll.harvard.edu/course/cs50-introduction-computer-science) 
# HeistGeist
### [Project Youtube video](http://example.com)
## Description:
**HeistGeist** is a top-down maze game that centers around a player character navigating through mazes diving deeper into increasingly dangerous and complex labyrinths for a prize well-worth the effort. The gameplay could be categorized as a rogue-like, but it has more in common with the likes of Pac-Man than spelunky for example. You take control of a skilled burglar making his way through a mansion and into heavily gaurded and forgotten depths no theif has dared to before.

### How it's built.
Heistgeist is built upon the quarter-century old but gold Python game library **[PyGame](https://www.pygame.org/news)**. The reason i chose to do things this way is because of its purely code-based ground-up framework, as well as past experiences with family and colleagues, making it the ideal ultimate project for a course dedicated to general programming. It lends itself to allot of hard work and effort, which just makes me more proud of the final product.

### Features.
The game has lots of interesting mechanics that make every successive run just as fun as the last. From powerups to enemies, here are just some.
1. #### A variety of powerups and items
    There is a vareity of different sorts of items, from bombs and rocket crossbows used to blow up paths through walls and enemies alike, to medkits and armor which boost survivability and allow you to tank damage, if you are being smart about it.
2. #### Infinite possibilities of maze combinations
    Every time you load a level, a maze is generated from scratch utilizing recursive algorithms and randomly spread out variated blocks and items accross the maze. No two mazes are alike, so  you can't just memorise the best path forward. As you make your way deeper, the maze gets more difficult as there are more things trying to kill you, and more maze to dig through. Along the way, there are also hazards, obstacles, and shortcuts which can help or hurt, depending on how luck chose to treat you.
3. #### Many enemies and just as many ways to kill them
    From blades to bombs to even an automatic rifle, There are many weapons that can assist you in clearing a path. Shoot a pair of bombs to blow a gaurd off his heels, or put down a gigantic bomb and watch as it turns walls to dust while hurling bomblets in every direction, destroying a nest of spiders in a fingersnap!

## The details

#### There are two main entities you must be aware of. They are:
* The spider: A quick bug that will sneak up behind you and take a bite faster than you can react. Be weary of their presence, and try to stay far especially at low health, but dont be afraid to rid them out with a slash or two from your shiv
* The gaurd: The protector and biggest threat of the deepest parts of the complex. Armed with powerful machine guns that can tear through any unsuspecting theives trying to find their way in. Very demanding to deal with, and very punishing to trip up around.

#### The mazes in HeistGesit are comprised of many different layers of multiple different themes. Which are in order:
1. The Front yard, a simple starting point from which to build on. Contains some hazards that can be avoided.
2. The House, The innerds of the property, empty of life but can be challenging to navigate with more credible danger.
3. The basement. Where the monster closets start. Some spiders here and there can give you a hard time, but some good stuff can help you deal with them. Difficult to run through, especially due to the numerous obstacles blocking your path
4. The caves. Lots of hurtful lava and many more spiders can be found here. It's too dark to see past your immediate surroundings, so its best to take a careful route through and choosing your fights well.
5. The dungeon. This is where the prize resides. Spiders are a hassle, but the real danger lies within the powerful gaurd enemies. Navigating around them is often a better idea than engaging them, but if you do choose to, it's best to do it strategically and thoughtfully.

The walls of the complexes are randomized with destructable pathways, hidden pathways, and hazardous surfaces that can  cause serious damage to careless runners. As you progress, there are less opportune gaps in the walls, replaced with dangerous damaging ones that take a good bite out of your health each time you brush up on them.


#### The game also includes the following powerups, along with each one being unlocked at certain depths and at certain times. They include:

* The medkit: Plain and simple, walk over it to regenerate all health in an instant. Most of the time it acts as a helpful boost, but when it save your life, you will  be glad you found it.
* The Powersneakers: These give you a fantastic boost in speed, as well as negating all stamina reduction and damage for a short period of time. Good for getting out of a real pickle.
* The bomb: The swiss army knife of the game. Blows through weakened walls with relative ease, and can cut through barriers, avoiding time losses and potential hazards, and even unlocking otherwise inaccessible paths. Useful for setting traps for enemies as well especially when grouped.
* The flaregun<sup>*</sup>: Use this to shoot a bright red star accross the maze, granting vision far past what is around you. Lights up the dark for a little while, so you can located points of interest and plot a path towards them.
* The Shiv<sup>**</sup>: Your best trusted tool. Nothing matches it in its efficiency of clearing out obstacles, wether that be some overgrowth or some arachnids. Does an alright job, but does it more reliably than anything else, as going without it most certainly means being stuck out in the open.
* The crossbow: A powerful weapon that can destroy walls and enemys alike from affar without putting yourself in harms way. Particularly useful for setting off huge chains of bombs while giving yourself enough time to take cover.
* The Mega-bomb: The big brother of the regular old bomb, with a few nephews so-to-speak. This bundle of tubes of chemicals has enough power to wreck through any wall, as well as a large area around it. As well as that, it scatters past the debris Lots of miniature bomblets that can cover a large area and hit targets far beyond what the bomb radius could hope to reach. Extremely powerful for demolition and dismbembering. Can't find a shortcut? Make your own!
* The armored suit<sup>***</sup>: A vital part of any late-game run. Provides unparalleled protection from most damage sources, allowing you to shrug off light hits and make heavier hits more managable. Keep it in good condition, because its the best protection to the dangers lurking.
* The flashlight: A humble flashlight. Holds a good charge, and is important for increasing your view far past the small radius you can usually see around. Use it and forget it, and when you find something far way with it, just know you couldn't have done it without it.
* The krinkov<sup>****</sup>: They say the best defense is a strong offense, and this is the best offense you can hope for. Fully automatic lead hose that can chew through spiders and even allow you to take the gaurds head-on. It's the best you could hope for in terms of weaponry, and while it may be rare, it will make dealing with the pesky gunmen a fair fight.
*  ???: A secret weapon that only the most dedicated can get to enjoy. Just try to be fast, and if you are lucky, you may uncover its power.
<br>*<sub>Only spawns at the depth of the number of apostrophes</sub>
### Footnote:
Created with the help of many tutorials and guides, as well as some insight given by AI chatbots. All code is original, but most of the assets have been taken off the internet and editted into something useful.
