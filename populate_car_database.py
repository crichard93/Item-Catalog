"""When run in Python 2, this file populates the car.db file with data. """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Model, User, Brand, Base

#Open a DB session named session
engine = create_engine('sqlite:///cars.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#Add myself as a User
user = User(name="Cory Richard", email="c.a.richard93@gmail.com")
session.add(user)
session.commit()


#Add Brand and Models
brand = Brand(name = "Acura", user = user)

session.add(brand)
session.commit()


model1 = Model(name = "RDX", description = """The 2018 Acura RDX debuts with its third generation, being faster,
    with premium cabin space and first-class cargo space, as well as a host of new Acura revolutionary technologies.
    Designed, developed and manufactured in America, the new RDX turbocharged will launch the fastest, best handling
    and most luxurious RDX ever. The new Acura RDX is powered by a turbocharged direct injection engine with a
    displacement of 2.0-liters, with DOHC VTEC and Dual Variable Timing Cam (Dual VTC). The maximum power is 272 hp
    (202 Kw) and 380 Nm (280 lb-ft) of torque.""", image = "acura_rdx.jpg", brand = brand, user = user)

model2 = Model(name = "RLX", description = """A redesigned Acura RLX large sedan was unveiled for 2018, overhauled to
    reflect the brand's new Precision Crafted Performance orientation in every detail. Said to be the most
    sophisticated and best performing Acura sedan to date, the 2018 model year RLX is fitted with the Sport Hybrid
    Super-Handling All-Wheel Drive technology also shared with the NSX supercar. Standard features on the 2018 RLX
    Sport Hybrid include premium Krell Audio System, Surround View Camera, parking sensors, LED fog lights, remote
    engine start, ventilated and heated front seats, heated rear seats and steering wheel and more.""", 
    brand = brand, image = "acura_rlx.jpg", user = user)

model3 = Model(name = "NSX", description = """Ten years after the original model went extinct, a new generation Acura
    NSX supercar debuted at the 2015 North American International Auto Show, being developed and produced in the US
    to bring a new experience in its segment. Closely following the lines of previous concepts, the 2016 Acura NSX
    amazes through sharp angles at both ends, which perfectly combine with the smooth surfaces that make the
    cockpit. This denotes a high level of precision and performance, making the car look dynamic even at a standstill.
    Naturally, the NSX's design is matched by the advanced underpinnings, using lightweight materials,
    third-generation magnetorheological dampers, double-joint front suspension, multi-link rear suspension,
    carbon-ceramic brakes and more. Unlike its predecessor, the second generation Acura NSX is powered by a hybrid unit,
    comprising three electric motors (two in front, one at the rear) and a twin-turbocharged V6 gasoline engine. The
    front works independently of the rear, which is controlled by a 9-speed automatic gearbox.""", 
    brand = brand, image = "acura_nsx.jpg", user = user)
session.add_all([model1, model2, model3])
session.commit()

#Add Audi Brand and Models
brand = Brand(name = "Audi", user = user)

session.add(brand)
session.commit()


model1 = Model(name = "A6", description = """The eighth generation Audi A6 was unveiled at the 2018 Geneva Motor Show
    bringing numerous innovations to the segment in terms of digitization, comfort, and sportiness. Part from the
    design refresh, the all-digital MMI touch response system allows central vehicle functions to be placed in the
    required position on the screen using drag-and-drop actions similar to smartphone use. Other new tech includes
    parking pilot, garage pilot, crossing assist, lane keeping assist, mild-hybrid technology, new all-wheel steering,
    and revised suspension.""", image = "audi_a6.jpg", brand = brand, user = user)

model2 = Model(name = "A8", description = """A new fourth generation Audi A8 was revealed in 2017 taking the brand's
    flagship model to a whole new level in terms of power, looks, and features. Visually, the biggest changes can be
    seen with the new hexagonal grille, headlights, aggressive bumpers, stoplights, and waistline. The interior is
    also all new being dominated by a new infotainment system. The Audi A8 is also the first production automobile in
    the world to have been developed for highly automated driving. From 2018, Audi will gradually be taking piloted
    driving functions such as parking pilot, garage pilot and traffic jam pilot into production.""",
    image = "audi_a8.jpg", brand = brand, user = user)

model3 = Model(name = "TT Roadster", description = """Ten years after the original model went extinct, a new generation Acura
    NSX supercar debuted at the 2015 North American International Auto Show, being developed and produced in the US
    to bring a new experience in its segment. Closely following the lines of previous concepts, the 2016 Acura NSX
    amazes through sharp angles at both ends, which perfectly combine with the smooth surfaces that make the
    cockpit. This denotes a high level of precision and performance, making the car look dynamic even at a standstill.
    Naturally, the NSX's design is matched by the advanced underpinnings, using lightweight materials,
    third-generation magnetorheological dampers, double-joint front suspension, multi-link rear suspension,
    carbon-ceramic brakes and more. Unlike its predecessor, the second generation Acura NSX is powered by a hybrid unit,
    comprising three electric motors (two in front, one at the rear) and a twin-turbocharged V6 gasoline engine. The
    front works independently of the rear, which is controlled by a 9-speed automatic gearbox.""", 
     image = "audi_ttroadster.jpg", brand = brand, user = user)

session.add_all([model1, model2, model3])
session.commit()

#Add Ford Brand and Models
brand = Brand(name = "Ford", user = user)

session.add(brand)
session.commit()


model1 = Model(name = "Mustang", description = """For the third time Ford offers Bullit a Special Edition, following
    previous version in the 2001 and in the 2008-2009 model years, to celebrated SteveMcQueen movie Bullit. The 2018
    Mustang Bullitt is based on the premium performance package of the Mustang GT that contains upgrades to the
    Brembo's six pistons front brakes, a Torsen limited slip differential, a larger rear anti-roll bar, and a bigger
    radiator to keep te bullitt's 5.0-liter V8 engine cool during extended chases. The upgraded v8 engine of 5.0
    delivers 475 HP (354 Kw) and 560 Nm (420 lb-ft) coupled allowing the new bullitt to reach a speed of 260 Kmh
    (163 mph).""", image = "ford_mustang.jpg", brand = brand, user = user)

model2 = Model(name = "Explorer", description = """In 2015, the fifth generation Ford Explorer got refreshed, coming
    with sharper looks and more technology. The biggest visual change can be observed at the front, where the SUV
    got new headlights, a new grille, bumper, hood, and lower air intakes. The trims levels have been overhauled and new
    tech made its way in, such as adaptive cruise control with collision warning and brake support, lane-keeping system,
    blind spot information system, cross-traffic alert, auto high-beams, inflatable rear safety belts and more. The
    suspension has been upgraded and there's a new 2.3-liter EcoBoost engine in the lineup.""",
    image = "ford_explorer.jpg", brand = brand, user = user)

session.add_all([model1, model2])
session.commit()

#Add Bugatti Brand and Model
brand = Brand(name = "Bugatti", user = user)

session.add(brand)
session.commit()


model1 = Model(name = "Chiron", description = """The new Bugatti Chiron Sport comes with a number of improvements to the
    chassis, but the engine remains the same as the Chiron, so the performance is almost the same. Bugatti made
    changes in a department where they needed serious improvements: the handlling. One of the modifications which make
    the Chiron Sport more nimble is a weight reduction of about 18 kg, thanks to the use of new lightweight parts.""",
    image = "bugatti_chiron.jpg", brand = brand, user = user)

session.add(model1)
session.commit()


#Add Honda Brand and Models
brand = Brand(name = "Honda", user = user)

session.add(brand)
session.commit()


model1 = Model(name = "Accord", description = """A new Honda Accord sedan was released for the American market in 2017
    representing the 10th generation of the model. The car is said to be built from the ground up featuring a lighter
    and more rigid body structure, two new turbocharged engines as well as the world first 10-speed automatic
    transmission for a front-wheel-drive car. As with the industry standards, the 2018 model year Honda Accord is
    also fitted with numerous safety and driver assist systems along with more car-connection technologies all
    contained in a more sophisticated, sleeker interior offering ample passenger and luggage space.""",
    image = "honda_accord.jpg", brand = brand, user = user)

model2 = Model(name = "Odyssey", description = """An all-new Honda Odyssey has been introduced in 2017 bringing a host
    of new features and technologies, including a new Magic Slide second row seats, new CabinWatch and CabinTalk, new
    Display Audio touchscreen, new Rear Entertainment System, and more. The Honda Odyssey's sophisticated and modern
    new styling adopts Honda's signature flying wing front grille flanked by available LED front headlights. The
    bold and sporty front fascia also conceals a new Active Shutter Grille for improved fuel efficiency when
    cruising. The Odyssey's signature lightning bolt beltline now provides an even more elegant design element with
    the sliding door tracks hidden in the lower portion of the rear quarter windows. At the rear there are LED
    taillights and an available new hands-free power tailgate with foot activation. Inside, the new Odyssey features
    high-grade materials including a soft-touch instrument panel. The driver's meter features a new 7-inch,
    full-color TFT display, and in the center of the dash there is an available 8-inch high-resolution Display
    Audio touchscreen interface (EX and above). In upper grades, stain-resistant leather first- and second-row
    seating surfaces and door trim and black carpeting and black seatbelts are designed to conceal stains, while a new
    grooveless tambour lid on the spacious and versatile center console resists the accumulation of crumbs and debris.""",
    image = "honda_odyssey.jpg", brand = brand, user = user)

model3 = Model(name = "NSX", description = """After ten years of absence on the market, a new generation Honda NSX
    supercar debuted at the 2015 North American International Auto Show, bringing a new experience in its segment.
    Closely following the lines of previous concepts, the 2016 Honda NSX amazes through sharp angles at both ends,
    which perfectly combine with the smooth lines that make the cockpit. This denotes a high level of precision
    and performance, making the car look dynamic even at a standstill. Naturally, the NSX's design is matched by
    the advanced underpinnings, using lightweight materials, third-generation magnetorheological dampers,
    double-joint front suspension, multi-link rear suspension, carbon-ceramic brakes and more. Unlike its predecessor,
    the second generation Acura NSX is powered by a hybrid drivetrain, comprising three electric motors (two in front,
    one at the rear) and a twin-turbocharged V6 gasoline engine. The front works independently of the rear,
    which is controlled by a 9-speed automatic gearbox. The car is identical to its Acura NSX American counterpart.""",
    image = "honda_nsx.jpg", brand = brand, user = user)

model4 = Model(name = "Civic", description = """The 10th generation Honda Civic sedan looks sportier than ever in
    2016. Virtually everything about the 2016 Civic Sedan is new - an all-new vehicle architecture, sporty and
    sophisticated new interior and exterior styling, a more spacious and high-quality cabin, two advanced new engines,
    and a host of new premium features and technologies. Lower, longer, wider and more muscular than the previous
    generation, its flowing lines, new signature chromed "wing" front fascia and available premium LED lighting,
    extended wheelbase and short overhangs brand the new Civic as a leader in its class, both technologically and
    in design.""",
    image = "honda_civic.jpg", brand = brand, user = user)

session.add_all([model1, model2, model3, model4])
session.commit()

print "Cars added to DB"

