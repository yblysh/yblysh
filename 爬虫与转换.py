# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 13:58:19 2021

@author: 博丽鸠
"""
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import tkinter
import os
import csv
import time
import xlrd
from tkinter import ttk
import tkinter.filedialog
import keyboard
import _thread

SKU=1
SKUtitle='A'
SILENCE = True
#daraz还是lazada,默认是daraz
DorL='d'
#chrome初始化
def set_spider_option(chromedriver_path=None) -> Chrome:
    # 调整chromedriver的读取路径，若不指定则尝试从环境变量中查找
    chromedriver_path = "chromedriver.exe" if chromedriver_path is None else chromedriver_path
    # 实例化Chrome可选参数
    options = ChromeOptions()
    # 静默启动 参数组策略
    if SILENCE is True:
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-software-rasterizer")
    # 其他推荐设置
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #禁止图片加载
    if DorL=='a':
        pass
        #options.add_argument('--blink-settings=imagesEnabled=false')
    #全屏启动
    options.add_argument('--start-maximized') 
    options.add_argument('--no-sandbox ')
    options.add_argument('--disable-javascript')
    return Chrome(options=options, executable_path=chromedriver_path)

#增加cookie
def add_cookie(driver,url):
    #加载然后写入cookie
    time.sleep(0.1)
    driver.get(url)
    driver.add_cookie({
        "domain":"aliexpress.com",
        "name":'cna',
        "value":'DrtGGFqZg08CAXjzcHvGbnoW',
        "path":'/',
        "expires":None
    })
    time.sleep(0.1)
    driver.get(url)
    time.sleep(0.1)


#输出
def output(dic,name):
    namedic={'Bags': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'Compartment', 'lock', 'Material', 'Waterproof', 'Recommended Gender', 'Dust Resistant', 'Closure type', 'Lockable', 'Case Type', 'Expandable', 'TSA Lock', 'Wheels', 'Laptop compartment', 'Laptop size', 'Set Size', 'Bag Shape', 'Clothing Material', 'Fa General Styles', 'Fa Pattern', 'Leather Material', 'Listed Year Season', 'Material Filter', 'Mens Trend', 'Occasion', 'Compatible Laptop Size', 'Number Of Pieces', 'Wallet Type', 'Lock Type', 'Gender', 'waterproof_function', "Women's Trend", 'Water Resistant', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Backpack capacity', 'Size', 'Bag Size', 'Color thumbnail', 'Case Size (mm)'], 'Came': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Promo Tag', 'Express delivery', 'Auto Focus Points', 'Battery Average Life', 'Video Capture Resolution', 'View Finder', 'Display Size', 'Type of battery', 'Optical Zoom', 'Megapixels', 'Wi-Fi Enabled', 'Type of Battery Group', 'Battery Charge Time', 'Rechargeable', 'Type of Camera Accessories', 'Design', 'Inner Material', 'Recommended Gender', 'Outer Material', 'Lockable', 'Remote Type', 'Wireless', 'Mobile Device Printing', 'Printer Connectivity', 'Film Type', 'Flash Range', 'Power Source', 'Camera Brand Compatibility', 'External Mount', 'Flash Modes', 'Device Compatibility', 'Writing Speed', 'Speed Class', 'Memory Card Type', 'Folded Length', 'Material', 'Maximum Operating Height', 'Weight Capacity', 'Sensor type', 'Body Only', 'Camera Accessories Included', 'Lens Kit', 'Lens Model', 'ISO Range', 'Max Shutter Speed', 'App-Controlled', 'Integrated Camera', 'Integrated GPS', 'Effective Pixels', 'Memory Card Compatibility', 'Autofocus', 'Compatible Film', 'Self Timer', 'Water Resistant', 'Number of Cameras', 'Storage Capacity', 'Minimum Age', 'Film Size', 'Number of Exposure', 'Picture Size', 'Lens Mount Compatibility', 'Maximum Aperture Range', 'Min Aperture', 'Maximum Aperture', 'Filter Diameter', 'Filter Type', 'Compatible With', 'waterproof', 'ISO Rating', 'Lens Diameter', 'Magnification', 'Focal Ratio', 'Focal Length', 'Car Camera Features', 'Number Of Channels', 'Number of Cameras Included', 'Recorder Channel Capacity', 'Security Camera Features', 'Security Camera Style', 'Security Camera Type', 'Connectivity', 'Number Of Sensors', 'Digital Zoom', 'Frame Rate (fps)', 'Power Supply', 'Optical Sensor Resolution (megapixels)', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Storage Capacity'], 'Char': ['Primary Category', 'Brand', 'Model', 'Digital', 'color', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color Family', 'Size'], 'Comp': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Barcode Ean', 'Cl Cable Length', 'Graphics Memory', 'Number Cpus', 'System Memory', 'Express delivery', 'Cable Type', 'Video Output', 'Connectivity', 'Cable Length', 'Lockable', 'Multimedia Playback Time (minutes)', 'Disk Type', 'Bluetooth Version', 'Number Of Connectable Devices', 'Power Consumption', 'Power Source', 'Compatible Laptop Size', 'Number of fans', 'Adjustable Fan Speed', 'Lighting Type', 'Usb Ports', 'Compatible Media', 'Drive Interface', 'DVD Read Speed', 'Wearing Type', 'Key Type', 'Power Capacity (mAh)', 'Screen Size (inches)', 'Rotatable', 'Model Compatibility for Mac', 'Power Adapter Type', 'Privacy', 'Screen Size', 'Mouse Type', 'Display Size', 'Maximum brightness (lumens)', 'Mounting Time', 'Display Features', 'Resolution', 'Response Time', 'Monitor Feature', 'RGB Lighting', 'Speaker Configuration', 'Brand Compatibility', 'Compatible Devices', 'Auto Shut Off', 'Cable Type', 'Output Voltage', 'Number Of Speakers', 'Number Of Sockets', 'Aspect Ratio', 'Device Placement', 'Maximum Resolution (MP)', 'Signal Type', 'Plug And Play', 'Power Output', 'Built in Microphone', 'Frame Rate (fps)', 'Image Capture Resolution', 'Case Type', 'Fan Speed (RPM)', 'Fan Type', 'Burner Type', 'Disc Size', 'Read Speed', 'Graphics memory', 'Wattage', 'Chipset Manufacturer', 'Gpu', 'Graphic Card Chipset', 'Graphic Card Model', 'Output Interface', 'Motherboard Memory Technology', 'Chipset', 'Data Rate', 'Form Factor', 'Number of memory slots', 'Sound Card', 'Number Of Pcie Slots', 'input voltage (V)', 'Number of SATA Cables', 'Cord Length', 'Number of CPU cores', 'Processor', 'Speed of Processor (GHz)', 'CPU Chipset Model', 'Computer Memory Type', 'Connectivity Speed (GHz)', 'System Memory', 'DDR Variant', 'Number Of Modules', 'Expansion Slots', 'Audio Output Mode', 'Number of channels', 'CPU Number cooling Type', 'Processor Type', 'AC Adapter', 'Input Output ports', 'Software Offerings', 'Wireless Connectivity', 'Touch Pad', 'Battery Life', 'Hard Disk (GB)', 'Operating System', 'CPU Speed (GHz)', 'Processor Type', 'Graphic Card', 'Camera Front (Megapixels)', 'CPU Cores', 'Memory Type', 'Storage Speed', 'Battery Type', 'No. of VGA Ports', 'No. of HDMI Ports', 'No. of USB 3.1 Ports', 'No. of USB 3.0 Ports', 'No. of USB 2.0 Ports', 'No. of Battery Cells', 'Backlit Keyboard', 'condition', 'Card Reader', 'Dimensions', '2 in 1 Type', 'storage_capacity_new', 'Wireless Signal Range (m)', 'Antenna Type', 'Network Connectivity', 'Number Of Lan Ports', 'Wireless Speed', 'Model Type', 'Number Of Bays', 'Usb Connectivity', 'Bus Type (bit)', 'Wireless', 'Wireless Transmission Speed', 'Transmission Speed', 'Network', 'Connectivity Type', 'Antennas', 'Ports', 'Frequency', 'Number of Ethernet ports', 'Type component switch', 'Usb Generation', 'Format', 'Genre', 'Platform', 'Printer Connectivity Type', 'Printer Function Type', 'Fax Color', 'Paper Tray Capacity (sheets)', 'Ink Package Type', 'Water Resistant', 'Cut Size', 'Number Of Pins', 'Maximum Print Resolution', 'Max Print Resolution Color', 'Mono/Color', 'Double Sided Printing', 'Input Tray Capacity (papers)', 'Paper Handling', 'Print Speed (CPM)', 'USB Support', 'Output Tray Capacity', 'Portable', 'Condition', 'ADF tray', 'ADF Capacity', 'Media Handling Capacity', 'Scan Resolution (DPI)', 'Scanner Function', 'Scanner Type', 'Customer Support', 'Number of Disc', 'Title', 'Compatible Operating System', 'Input Type', 'Connector Type', 'Storage Drive Type', 'Connectivity', 'Storage Size', 'Type', 'Writing Speed', 'Bay Drive Size', 'Ssd Form Factor', 'NAS Number of Bays', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Writing Speed (MB)', 'Fan Dimensions'], 'Digi': ['Primary Category', 'Brand', 'Model', 'SMS or Email', 'Location', 'City', 'Color Family', 'City', 'Location Address', 'Pax', 'Type of Spa/Beauty Service', 'Valid From (dd/mm/yyyy)', 'Valid To (dd/mm/yyyy)', 'Routes', 'Type of Courses', 'Seminar Type', 'Type of theme park', 'Type of Fitness Accessories', 'Fitness Type', 'Sport Type', 'Type of Sport Accessories', 'Brand', 'Store', 'Type of Restaurant', 'Entertainment Type', 'Subscription/Card Type', 'Game Key Type', 'Game Platform', 'Gift Card Type', 'Software Type', 'Tour type', 'Service Provider', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Box Dimensions', 'Product Category', 'Quality of Photoshoot', 'Service Type'], 'Fash': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Age Range', 'Campaign', 'Color Code Brand', 'Color Name Brand', 'Complementary Products', 'Main Material', 'Material Family', 'Season', 'size', 'Express delivery', 'Size Chart', 'Belt Material', 'Clothing Material', 'Collar Type', 'Kid years', 'Toe Shape', 'Leather Material', 'Pattern', 'Shoes Closure Type', 'Boot Height', 'Boot Type', 'Material', 'Occasion', 'Number Of Pieces', 'Style', 'Accessory Type', 'Belt Styles', 'Accessories', 'Hair Accessories', 'Hat Brim Styles', 'Hat Style', 'Umbrella Category', 'Pants Fly', 'Length', 'Waist Type', 'Bottom Type', 'Skirt Length', 'Dress Shape', 'Dress Length', 'Sleeves', 'Blouse Sleeve Style', 'Hoodie Style', 'Jacket Coat Style', 'Jacket Closure Type', 'Sock Tight Style', 'Swimwear Style', 'Top type', 'Underwear Style', 'Sleep Style', 'Heel Height (cm)', 'Type of heels', 'Shoes Decoration', 'Shoe Type', 'Sneaker Height', 'Sneaker Type', "Men's Trend", 'Scarf Style', 'Tie Width', 'Bag Shape', 'Tee Neckline', 'Fit Type', 'Sleeve Length', 'Neckline', 'Wash Color', 'Fit Type', 'Jeans Decoration', 'Jeans Fit Type', 'Fit Type', 'Swimwear Style', 'Underwear Style', 'Sleep Style', 'Length', 'Shalat Style', 'Men Shoes Closure', 'size_wear', 'Accessory Type', 'Sneaker Upper Height', 'Sneakers Style', 'Wallet Type', 'Beach Style', 'Tee Sleeve Length', "Women's Trend", 'Sleeve Length', 'Bottom Style', 'Clothing Decoration', 'Intimate Type', 'Bra Type', 'Swimwear Style', 'Swimwear Type', 'Top Type', 'Skirt Style', 'Piece Count', 'Bra Accessories', 'Lingerie Style', 'Panty Type', 'Shaper Style', 'Accessory Type', 'Dress Style', 'Hijab Style', 'Top Style', 'Sandal Type', 'Sneaker Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Collection', 'Color', 'Designer', 'Features', 'Occasion', 'Material Filter', 'Listed Year', 'Color thumbnail', 'Model Height', 'Size Model is Wearing', 'Size Baby Clothing', 'Top Style'], 'Furn': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Assembly Type', 'Seat Count', 'Shelf Life Managed', 'artist_name', 'Material', 'Number of Pieces', 'Storage Feature', 'Bed Type', 'Net Depth (mm)', 'Net Height (mm)', 'Net Width (mm)', 'Number of Drawers', 'Dresser Design', 'mattress_size', 'Size', 'Core Construction', 'Wardrobe Blocks', 'Wardrobe Door Type', 'Wardrobe Materials', 'Pattern', 'Drawer Paper Size', 'Orientation', 'Style', 'Chair Arms', 'Chair Back Height', 'Coasters', 'Desk Chair Type', 'Upholstery', 'Desk Design', 'Desk Features', 'Desk Shape', 'Recommended Gender', 'Frame Material', 'Kids Bed Design', 'Kids Bed Size', 'Bookcase design', 'Number of Shelves', 'Chair Type', 'Kids Desk Features', 'Kids Desk Type', 'Kids Storage Type', 'Chair Back Panel Style', 'Stool Height', 'Shape', 'Table Base', 'Chair Design', 'Table Features', 'Table Height', 'Dining Table Type', 'Number of Seats', 'Kitchen Island Design', 'Kitchen Island Features', 'Assembly', 'Max TV Size', 'Furniture Features', 'Ottoman Design', 'Sofa Type', 'Assembly Required', 'Outdoor Chair Type', 'Water Resistant', 'Outdoor Table Type', 'Shade Fabric', 'Shade Features', 'Scent', 'Clock Type', 'Curtain Type', 'Curtain Features', 'Curtain Length (mm)', 'Curtain Material', 'Curtain Type', 'Curtain Width (mm)', 'Cover Material', 'Cushion Type', 'Finish', 'Mirror Features', 'Mirror Type', 'No Of Pictures', 'Foldable', 'Rug Make', 'Rug Pile', 'Rug Shape', 'Rug Type', 'Painting Shape', 'Category', 'Power Source', 'Light Features', 'Light Type', 'Light Bulb Colour', 'Light Bulb Type', 'Light Bulb Wattage (w)', 'Lockable', 'Number Of Compartments', 'Type', 'Washable', 'Storage Tub Features', 'Storage Tub Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Bedding Size'], 'Groc': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'dMart', 'Storage Requirements', 'Country Of Origin', 'volume', 'weight', 'Pack Size', 'Freshness', 'Shelf Life', 'Packaging Type', 'Drink Type', 'Pasta Shape', 'Rice Type', 'City', 'Season', 'Vegetable Type', 'Frozen', 'Paper Type', 'SMS or Email', 'Glass Type', 'Number of Bottles', 'Volume (ml)', 'Alcohol Percentage', 'Age (years)', 'Limited Edition', 'Type of Cognac', 'Type of Gin', 'Type of Rum', 'Type of Tequila', 'Whisky Style', 'Whisky Type', "Wine Advocate's rating", 'Food Pairing', 'Grapes (for Finest Wines)', 'Organic', 'Country of Origin', 'Body', 'Grapes (for Red wines)', 'Vintage', 'Grapes (for White wines)', 'Type of Bundle', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'flavor', 'Country of Origin', 'Maximum Shelf Life'], 'Heal': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Beauty Features', 'Capacity Slices', 'Hair Type', 'Health Features', 'Health Format', 'Express delivery', 'dMart', 'Storage Requirements', 'volume', 'weight', 'Pack Size', 'Shelf Life', 'Country of origin', 'Fragranced', 'Country of origin', 'Brand Classification', 'Ideal Usage', 'Pack Type', 'Concerns', 'Travel Size', 'Product Form', 'Product Form', 'Product Form', 'Skin Type', 'Formulation', 'Sun Protection (SPF)', 'Warranty', 'Tools Power Source', 'Wattage (W)', 'Usage', 'Skin Concerns', 'Days of Supply', 'Product Form', 'Flavor', 'Ingredient', 'Malaysia Authorized License', 'Recommended Gender', 'Aftershave', 'Attar', 'Body_Spray', 'Cologne Type', 'Eau_De_Cologne', 'Eau_De_Parfume', 'Eau_De_Toilette', 'Extrait_de_parfum', 'Fragrance_Sets_and_Minis', 'stick_deodorant', 'Hair Care Benefits', 'Product Form', 'Hair Color Type', 'Ingredient Hair Oil', 'Product Form', 'Texture', 'Vegan', 'Product Form', 'Eyes Makeup Finish', 'Benefits', 'Mascara Benefits', 'Face Makeup Finish', 'Skin Tone', 'Face Makeup Benefits', 'Face Makeup Coverage', 'Product Form', 'fmlt makeup', 'Lips Makeup Finish', 'Lips Makeup Benefits', 'Product Form', 'Area Of Use', 'Country of Origin', 'Body Scrub Formulation', 'fmlt skin care', 'Skin Care Benefits', 'Age Group', 'Product Form', 'Optical Power (Diopter)', 'Lens Replacement Frequency', 'Flow Level', 'Scent Feature', 'Wings', 'Oral Care Benefits', 'Product Form', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Scent', 'Shade', 'Color Group', 'Color', 'Waterproof', 'Pack Size'], 'Home': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Home Features', 'Horse Power', 'Imported', 'Express delivery', 'Capacity', 'power_consumption', 'Purification Method', 'Horsepower', 'Inverter', 'Type Air Conditioner', 'Room Size', 'Air Conditioner Rated Capacity (BTUs)', 'Air Conditioner Features', 'Connecting Wire', 'Kit Included', 'Fan Speed (RPM)', 'Air Cooler Features', 'Wattage', 'Air Purifier Filtration Type', 'Carbon Filter', 'Ionizer', 'Virus Killer', 'HEPA Filter', 'De-humidifier Capacity (ml)', 'Air Humidifier Parts Type', 'Humidifier Type', 'Air Humidifier Features', 'Blade Side (inches)', 'Number Of Blades', 'Fan Features', 'Fan Type', 'Overheat Control', 'Water Heater Type', 'Auto Shut Off', 'Drip Stop', 'Indicator Light(s)', 'Input voltage', 'Garment Steamer Type', 'Soleplate Type', 'Plate', 'Spray', 'Temparature Control', 'Iron Type', 'Number of Stiches', 'Sewing Speed', 'Number of hobs', 'Type of induction cooktops', 'Type of infrared cooktops', 'Cooktop Surface', 'Cooktop Type', 'dishwasher_type', 'Auto Defrost', 'color', 'Freezer Type', 'Refrigerator Features', 'cooking_modes', 'oven_capacity', 'power_consumption_microwave', 'microwave_type', 'microwave_features', 'Wall Oven Type', 'Range Mount Type', 'Number of doors', 'Nofrost system', 'Refrigerator Type', 'filter_type', 'purification_capacity', 'number_of_filters', 'Other Cooking Features', 'Power Consumption (Grill)', 'Cubit feet', 'Fridge Configuration', 'Spin speed (rpm)', 'Digital Display', 'Maximum Spin Speed (RPM)', 'Top Type', 'Type Washing', 'Washing Capacity (kg)', 'Washing Features', 'Washing Mode', 'Sewing Machine Type', 'Sewing Machine Features', 'Bakeware Material', 'Non-stick Surface', 'Number of waffles', 'Waffle thickness', 'Milk Frother', 'Grinder_Type', 'Coffee Machine Type', 'Pot Material', 'Operating Mode', 'Power (watt/horsepower)', 'Jug Material', 'Settings', 'Capacity (ML)', 'With Grinder', 'Food Processor Type', 'Mixer Type', 'Jar Material Type', 'Type of Juicer', 'Type of Rice Cooker', 'type_of_battery', 'blower', 'cord_length', 'wheels', 'vacuum_cleaner_type', 'adjustable_suction', 'vacuum_cleaner_features', 'Drum Type', 'Washing Machine Type', 'Dryer Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail'], 'Kitc': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'dMart', 'capacity', 'Baking Dish Type', 'Cookware Features', 'Cookware Shape', 'Cookware Capacity', 'Baking Utensil Type', 'Cake Pan Type', 'Baking Tray Type', 'Number of Pieces in Set', 'Coffee Maker Type', 'Coffee Accessory Type', 'Power Consumption (W)', 'Home Features', 'Horse Power', 'Imported', 'Tea Accessory Type', 'Teapot Capacity (Cups)', 'Coffee/Tea Server Type', 'Pan Type', 'Cookware Length (cm)', 'Roasting Tray Type', 'Cookware Diameter (cm)', 'Stovetop Kettle Features', 'Cookware Finish', 'Number of Pieces', 'Cutlery Type', 'Shape', 'Dinner Plate Type', 'Pattern', 'Material', 'Mug Type', 'Barware Type', 'Jug Type', 'Specialty Glass Type', 'Linen Fabric', 'Linen Accessory Type', 'Pot Rack Type', 'Cheese Tool Type', 'Strainer Type', 'Cooking Utensil Type', 'Fruit Tool Type', 'Measuring Tool Type', 'Meat Tool Type', 'Rust Resistant', 'Oil Tool Type', 'Thermometer Type', 'Dishwasher Safe', 'Serving Bowl Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Cookware material', 'Material', 'Service Size', 'Water Holding Capacity (L)'], 'Laun': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'Adjustable Handle', 'Broom Type', 'Flexible Head', 'Spinmop Features', 'Brush Type', 'Machine Washable', 'Material', 'Bin Type', 'Capacity', 'Wheel Support', 'Assembly Required', 'Dryiing Rack Materials', 'Drying Rack No. of Rails', 'Rust Proof', 'Foldable', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail'], 'Live': ['Primary Category', 'Brand', 'Model', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8'], 'Medi': ['Primary Category', 'ISBN/ISSN', 'Brand', 'Model', 'Color Family', 'Format', 'Gender', 'Genderfilter', 'Genre', 'Isbn', 'Media Features', 'Express delivery', 'Edition', 'Language', 'Listening Length', 'Number of pages (pages)', 'Publisher', 'Version', 'Year', 'Age Group', 'Edition Type', 'Format Magazines', 'Issue', 'Format', 'Age Restriction', 'Date of publishing', 'Artist', 'Instrument Key', 'Instrument Range', 'Type Concert Percussion', 'Type', 'Number of Fret', 'Type Woodwinds', 'Set Size', 'drums_set', 'pedals_types', 'Body Finish', 'Body Material', 'Bridge System', 'Fretboard Material', 'Neck Material', 'Pickup Configuration', 'Number of Key', 'File Size', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Author', 'Color thumbnail'], 'Mobi': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'Network Type', 'Sim Slots', 'Sim Type', 'Price Range', 'Landline Features', 'Speaker Phone', 'Batteries Included', 'Connection', 'Cable Length', 'Compatible Devices', 'Cable Type', 'Data Transfer Rate', 'Memory Storage Capacity', 'Speed Class', 'Card Type', 'Cable Included', 'Charging Interface', 'Number of Ports', 'Output Power', 'Compatible Products', 'Mount Features', 'Mount Type', 'Connector', 'Dock Connector', 'Dock Features', 'Accessories Style', 'Transfer Speed', 'Replacement Type', 'Battery Capacity', 'Batteries Required', 'Number Of Flashes', 'Case Material', 'Type (case/cover)', 'Powerbank Features', 'Input Type', 'Charging Cable Included', 'Material', 'Type of Screen Guard', 'Number Of Layers', 'Wireless Connectivity', 'Remote Included', 'Case Function', 'Tablet Connection', 'Stylus Features', 'Brand Compatibility', 'Wattage', 'Connectivity', 'Wireless Charging Type', 'Phone Features', 'PPI', 'Processor Type', 'Screen Size (inches)', 'Screen Type', 'Video Resolution', 'Network Connections', 'RAM Memory', 'Type of battery', 'Camera Back (Megapixels)', 'Camera Front (Megapixels)', 'Operating System', 'Resolution', 'E-Warranty', 'Number Of Cameras', 'Notchted Display', 'Fast Charging', 'Headphone Jack', 'Wireless Charging', 'Protection', 'Body Type', 'Year', 'Number Of Cores', 'Operating system version', 'Phone Processor Type', 'Phone Type', 'Condition', 'Touchpad', 'Cellular', 'Expandable Memory', 'Screen Size (inches)', 'Tablet Features', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color Thumbnail', 'Compatibility by Model', 'Powerbank Capacity'], 'Moth': ['Primary Category', 'Storage Requirements', 'Brand', 'Model', 'Color Family', 'Express delivery', 'dMart', 'Pack Size', 'Country of Origin', 'weight', 'Shelf Life', 'Recommended Age', 'Gender', 'Type of Baby Carrier', 'Weight Capacity', 'volume', 'Organic', 'Thermometer Type', 'Dietary Requirements', 'Flavor', 'Age Group', 'Form', 'Type of Bodywash', 'Foldable', 'Occasion', 'Featured Characters Brand', 'Costume Theme', 'Featured Game', 'Recommended Gender', 'Outer Material', 'Type of Diaper Bags', 'Type Diaper', 'Count (pieces)', 'washable', 'Type of Breastpumps', 'Wattage', 'Portable', 'Flavor Nutrition', 'Number Of Pages', 'Listed Year Season', 'Pants Fly', 'Clothing Style', 'Bottom Style', 'Length', 'Pattern', 'Waist Type', 'Clothing Material', 'Pant Style', "Women's Trend", 'Clothing Decoration', 'Dress Shape', 'Collar Type', 'Dress Length', 'Sleeves', 'Sleeve Length', 'Intimate Type', 'Bra Type', 'Swimwear Style', 'Swimwear Type', 'Top Style', 'assembly_required', 'size_steel', 'Baby Recommended Age', 'Mattress Size', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Size Baby Clothing', 'Size Baby Sho', 'Size Diaper', 'Diaper Pack Size', 'Volumetric', 'Size'], 'Pet ': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'dMart', 'Storage Requirements', 'Country Of Origin', 'volume', 'weight', 'pack size', 'Shelf Life', 'Lockable', 'Type of Bird Cage Accessories', 'Pets Flavor', 'Food Type', 'Bed Type', 'Washable', 'Food Capacity', 'Type of Feeders', 'Cat Age', 'Cat Life Stage', 'Food Feature', 'Cat Breed', 'Type of Cat Toys', 'Soil Type', 'Dog Breed Type', 'Dog Life Stage', 'Dog Size', 'Type of Veterinary Diet', 'Activity Type', 'Type of Dog Toys', 'Type of Leash', 'Pet Type', 'Shape', 'Tank Capacity', 'Type of Reptile Food', 'Type of Reptile Habitats', 'Type of Small Pet Food', 'Type of Small Pet Habitat Accessories', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Size of Beds', 'volumetric capacity', 'Pet Food Bag Size', 'Pet Size', 'Dog Age', 'Dog Weight'], 'Samp': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Category String', 'Cost', 'Creation Source Config', 'Creation Source Simple', 'Delivery Cost Supplier', 'Delivery Time Supplier', 'Display If Out Of Stock', 'Erp Item Category Code', 'Erp Product Group Code', 'Erp Updated At', 'Manufacturer Txt', 'Marketplace Children Skus', 'Marketplace Parent Sku', 'Max Delivery Time', 'Merchant Price', 'Min Delivery Time', 'Min Order Quantity', 'Modeiswearing', 'Modelbodymeasurements', 'Note', 'Orderdate', 'Original Price', 'Package Pieces', 'Package Type', 'Ponumber', 'Production Country', 'Product Line', 'Product Measures', 'Product Owner', 'Product Type', 'Shipmenttype', 'Shipment Cost Item', 'Shipment Cost Order', 'Shipment Type', 'Sku Source', 'Sku Supplier Config', 'Source Cost 1', 'Source Cost 2', 'Source Cost 3', 'Source Image Url', 'Source Ship Cost 1', 'Source Ship Cost 2', 'Source Ship Cost 3', 'Source Ship Time 1', 'Source Ship Time 2', 'Source Ship Time 3', 'Source Stock 1', 'Source Stock 2', 'Source Stock 3', 'Source Url 1', 'Source Url 2', 'Source Url 3', 'Status', 'Status Source', 'Status Supplier Config', 'Status Supplier Source', 'Supplier', 'Supplier Name', 'Supplier Simple', 'Supplier Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8'], 'Serv': ['Primary Category', 'Brand', 'Model', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Number of Pictures Per SKU', 'Picture Quality', 'Product Category', 'Service Type'], 'Spor': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Sports Features', 'Sport Type', 'Express delivery', 'Liquid Capacity (OZ)', 'Backpack capacity', 'Applicable Area', 'Exercise Type', 'Size', 'foldable', 'inclination', 'Auto Incline', 'Batteries Required', 'Maximum Weight Capacity', 'Material Type', 'Bluetooth Version', 'Strap Material', 'Energy Rating', 'Required Serial', 'Refresh Rate', 'wear_acc_strap_material', 'Ball Size (cm)', 'Length (inches)', 'Thickness (mm)', 'Width (inches)', 'Size (feet)', 'Weight (kg)', 'Adjustable', 'Weight', 'Weight Type', 'Adjustable', 'Sold in', 'Dimensions', 'Anti Slip', 'Bundesliga Teams', 'Football Championships', 'La Liga Teams', 'Premier League Teams', 'Series A Teams', 'Recommended Gender', 'Tracker Styles', 'Compatible Operating System', 'Bluetooth', 'Electronics Features', 'Size', 'Sleeping Capacity (number of persons)', 'Number of Speed', 'Age Group', 'Gears', 'Size Helmet', 'Fishing Type', 'Bag Type', 'Hand Orientation', 'Recommended User', 'Racquet Material', 'Racquet Stringing', 'Activity Type', 'Kid years', 'Cup Size', 'Top type', 'Platform Height (cm)', 'Swimwear Type', 'Form', 'Baseball Bat Length', 'Throwing Hand', 'Floaties Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Clothing Size', 'Glove Size   ', 'Size', 'Display Resolution', 'Bike Frame Size (inches)', 'Kids Bike Age', 'Glove Size   ', 'Fishing Rod Length (meter)', 'Shaft material', 'Shoes Size   ', 'Board Type'], 'Test': ['Primary Category', 'Brand', 'Model','Color Family','Express Delivery', 'D-Mart', 'Routes', 'usb_connectivity', 'washable', 'category_product', 'SMS or Email', 'test Warranty Type', 'Test Normal2', 'Engine displacement (cc)', 'Battery Type', 'manufacturing_year', 'registration_city', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Box Dimension', 'color_family', 'size', 'Wholesale', 'Size_chart', 'Subscription test、', 'Photoshoot Quality', 'Number of Pictures', 'Service Type', 'Color thumbnail'], 'Tool': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'size', 'Capacity Battery', 'Battery Core Type', 'Battery Features', 'Input Voltage', 'Cable Type', 'Other Electrical Type', 'Electrical Tool Type', 'Maximum Current', 'Powerpoint Type', 'Fire Alarm Power Type', 'Fire Alarm Type', 'Fire Blanket Features', 'Fire Blanket Length (m)', 'Fire Ladder Length (m)', 'Material', 'Fire Extinguisher Class', 'Fire Extinguisher Features', 'Fire Extinguisher Medium', 'Fire Extinguisher Size (Kg)', 'Bathroom Fitting Type', 'Finish', 'Bathroom Tapware Type', 'Plumbing Tapware Features', 'Plumbing Tapware Finish', 'Plumbing Fixture Type', 'Pipe Fitting Type', 'Kitchen Fitting Type', 'Kitchen Tapware Type', 'Socket Type', 'Fastener Head Style', 'Fastener Length (mm)', 'Fastener Surface Type', 'Fastener Type', 'Fastener Maximum Weight (kg)', 'Cable Type', 'Ladder Type', 'Number of Sockets', 'Wheels', 'outdoor Power Tool Accessory', 'Outdoor Power Tool Type', 'Plumbing Components', 'Insect Control Type', 'Measuring Tool Type', 'Power source', 'Assembly Required', 'Adhesive Product Type', 'Cable Length', 'Glue Type', 'Phone Screen Size', 'Screen Size', 'TV Screen Size', 'Tablet Screen Size', 'Caulking Category', 'Caulking Type', 'Carpet Type', 'thickness of mattress', 'Floor Adhesive Type', 'Tile Type', 'Timber Type', 'Vinyl Type', 'Paint Accessory Type', 'Paint Colour Tone', 'Paint/Stain Key Features', 'Paint Finish', 'Paint Product Range Variation', 'Paint Surface Type', 'Paint Type', 'Washable', 'Sealer Finish', 'Sealer Product Range', 'Sealer Surface Type', 'Sealer Usage', 'Window Hardware Type', 'Amperage (amp)', 'Cordless', 'No. of included Batteries', 'Power Tool Feature', 'Tool compatible with Surfaces:', 'Tools Included', 'Drill Type', 'Extractor Type', 'Grinder Type', 'BTU Rating', 'Torque (lb-in)', 'Power Tool Accessory Type', 'Disc Size (inches)', 'Saw Type', 'Welder Type', 'Protective Clothing Features', 'Protective Shoe Features', 'Door Hardware Type', 'Security System Type', 'Lock Type', 'Peril Type', 'Safe type', 'Tool Storage Type', 'Features', 'Light Bulb Type', 'Lumens (lm)', 'Light Bulb Wattage (w)', 'Worklight Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'size_steel', 'Color thumbnail', 'Size Paver', 'Paint Volume (L)'], 'Toys': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Toys Characters', 'Toys Features', 'Trend', 'Express delivery', 'Recommended Age', 'Game Type', 'Interest', 'Recommended Gender', 'Baby Recommended Age', 'Rechargeable', 'Doll Size', 'Type of Playset', 'Battery Required', 'Battery Capacity', 'Types of S.T.E.M Toys', 'Battery Type', 'Assembly Required', 'Sports Type', 'Type of Card Games', 'Featured Game', 'Number Of Players', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail'], 'TV, ': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Display Resolution', 'Electronics Features', 'Energy Rating', 'Refresh Rate', 'Required Serial', 'Speakers Config', 'Express delivery', 'Activity Type', 'Compatible Operating System', 'Battery Included', 'Rechargeable', 'Wearing Type', 'connector_1', 'wireless_connectivity', 'Battery Capacity', 'Bluetooth Version', 'Charging Time', 'Compatible Devices', 'Functions', 'Runtime', 'Standby Time', 'Headphone Accessories', 'Headphone Features', 'Bluetooth', 'Cable Length', 'Bookshelf Speaker Type', 'Output Connectivity', 'Speaker Features', 'Woofer Size', 'Hi-Fi Connectivity', 'Home Entertainment Features', 'Designed For', 'Power Source', 'Cable Type', 'Cable Length', 'Input Connectivity', 'Receiver Features', 'Number of channels', 'Karaoke Features', 'Karaoke Type', 'Mic Connectivity', 'Microphone Inputs', 'Subwoofer', 'Speaker Connectivity', 'Turntable Type', 'Number of Speeds', 'DAC Connection Type', 'Mic Accessories', 'Mic Types', 'Channel Quantity', 'Power Source Type', 'Built-in Battery', 'Radio Features', 'Radio Type', 'Power Supply', 'Capacity', 'External Storage', 'Recorder Connectivity', 'Recorder Types', 'Portable Speaker Features', 'Console Model Compatibility', 'Case Type', 'Internal Memory', 'Console Model', 'Game Genre', 'Platform Type', 'Nicotine Level', 'E-Cigarette Material', 'E-Cigarette Type', 'Screen Type', '3D Glasses Type', 'Remote Included', 'Suitable For Devices', 'Wired', 'Antenna Type', 'TV Adapter Type', 'TV Receiver', 'Universal', 'Load Capacity (kilograms)', 'TV Size', 'Wall Mount Features', 'tv_resolution', 'HDMI Ports', 'USB Ports', 'Resolution', 'Display Size (inches)', 'Curved TV', 'Cinema 3D', 'Smart TV', 'Number of USB ports', 'TV Technology', 'BluRay 3D Features', 'BluRay Features', 'Portability Features', 'Decode Ability Type', 'Media Player Type', 'Battery Required', 'Display', 'File Formats', 'Media Streaming', 'Video Player Type', 'Projector Type', 'Model Compatibility', 'Strap Material', 'Material Type', 'Tracker Style', 'Watch Features', 'Watch Features', 'Compatible Os', 'Smart Glasses Features', 'Dial Size (mm)', 'Storage Space', 'Generation', 'Display Type', 'Movement', 'Gadget Compatibility', 'Virtual Reality Features', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Watch Size'], 'Bedd': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'Shape', 'Pattern', 'Towel Material', 'Water Resistant', 'Towel Size', 'Mounting', 'Finish', 'Material', 'Type Digital', 'Net Depth (mm)', 'Net Height (mm)', 'Net Width (mm)', 'Number of Shelves', 'Shelf Design', 'Storage Feature', 'Curtain Features', 'Curtain Length (mm)', 'Curtain Material', 'Transparency', 'Bed Sheet Type', 'Linen Fabric', 'Thread Count', 'Bed Accessory Type', 'Filling', 'Core Construction', 'Pillow Shape', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Bedding Size', 'Mattress Size'], 'Moto': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Additives', 'Services', 'Volumetric Capacity', 'Flushes', 'Greases type', 'Lubricant type', 'Engine Oil Type', 'Viscosity', 'Make', 'Year', 'Clutches & Parts type', 'Transmission & Parts type', 'Air Conditioning type', 'Relays', 'Axle Type', 'Power Steering type', 'Rack & Pinion type', 'Display', 'Switches', 'Hubcap Size', 'Hubcaps, Trim Rings & Hub Accessories type', 'Lug Nuts & Accessories type', 'Snow Chains type', 'tires_variation', 'Stain Resistant', 'Bearing number', 'Wheels Size', 'Wheels Type', 'Wheel Material', 'Brake & Repair Tools type', 'Cloths & Towels type', 'Battery Voltage', 'Function Power', 'Measuring Tools type', 'Pullers type', 'Steering & Suspension Tools type', 'Battery Accessories Type', 'Interface type', 'Form Gel', 'Liquid Expiration Date', 'Type Care', 'CB Radios & Scanners type', 'Cable Type', 'Screen Size', 'Touchscreen', 'video_capture_resolution', 'megapixels', 'type_of_battery', 'Promo Tag', 'Body Armor type', 'Cargo Management type', 'Hood type', 'License Plate Covers & Frames type', 'Function Light', 'Spoilers, Wings & Styling Kits type', 'Trailer Accessories type', 'Truck Bed & Tailgate type', 'Car Polishes & Waxes type', 'Type Paint', 'Paints & Primers type', 'Refill Included', 'Antitheft type', 'Patterned', 'Consoles & Organizers type', 'Seat Cover type', 'Interior accessories material', 'Position', 'Material', 'Style Helmet', 'Recommended Gender', 'Style Jacket', 'Waterproof', 'Function Paint Body', 'Type Brake', 'Type Vehicle', 'Type exhaust system', 'Type Filter', 'Type Lighting', 'Deflectors & Shields type', 'Grilles & Grille Guards type', 'Performance & Air Intakes type', 'Running Boards & Steps type', 'Shocks, Struts & Suspension type', 'Tonneau Covers type', 'Towing and Winches type', 'Engine Displacement Cc', 'Model Year', 'Transmission', 'Variant', 'Fuel Type', 'Registration City', 'Registration Year', 'Body Type', 'Model', 'Mileage', 'Location', 'assembly', 'Type Sport', 'Power', 'Power Consumption (W)', 'Port', 'Type Toys', 'Motorcycle Make', 'Moto Tire Sizes', 'Engine Oil Grade', 'Stroke oils', 'Chest&Back Protectors Type', 'footwear_size', 'footwear_type', 'Availability Of Pin-Lock', 'Availability Of Sun Visor', 'Quality Certification', 'Shell Material', 'Helmets Type', 'Jacket Material', 'Number of Cylinders', 'Number of Gears', 'location_city', 'Available Location by Postal Code', 'Motor Type', 'Finish', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Tire Model', 'Memory Size', 'Size Wear', 'Size'], 'OPS ': ['Primary Category', 'Brand', 'Model', 'City', 'Routes', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Box Dimensions'], 'Pack': ['Primary Category', 'Brand', 'Model', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8'], 'Stat': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'Types of Easels', 'Sheet Size', 'Bristles of Brush', 'Painting Brush Types', 'Size', 'Types of Paper', 'Pencil Lead Degree (Hardness)', 'Event', 'Cartridge Printer Paper Type', 'Number of Pieces in Set', 'Carton', 'Number of Sheets per Ream', 'Paper Features', 'Thickness (gsm)', 'Number of Pages', 'Diary Type', 'Envelope Type', 'Sticky Label Feature', 'Sticky Label Type', 'Notebook Features', 'Notebook Type', 'Flag Type', 'Binder Type', 'Pattern', 'Board Type', 'Calculator Power Source', 'Calculator Type', 'Clip Type', 'Desk Organizer Type', 'Material', 'Binder Edge Type', 'Filing Type', 'Glue Type', 'Labelmaker Printing Type', 'Labelmaker Type', 'Cutter Type', 'Staple Type', 'Fastener Type', 'Tape Type', 'Correction Type', 'Marker Type', 'Pen Thickness', 'Pencil Hardness', 'Pencil Type', 'Pen Type', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Paper Type', 'Number of Subjects'], 'Watc': ['Primary Category', 'Brand', 'Model', 'Color Family', 'Express delivery', 'Lens Type', 'Frame Material', 'Lens Power', 'Frame type', 'Shape', 'Lens quality', 'Sunglasses lens type', 'Material', 'Occasion', 'Coloured gems type', 'Diamond Clarity', 'Diamond colour', 'Diamond cut', 'Main diamond carat size', 'Product Size', 'Main stone', 'Jewellery Packaging and Display Type', 'Jewellery tool & equipment type', 'Dial Size', 'Watch Case Size (mm)', 'Movement', 'Strap Material', 'Watch Case Shape', 'Watch Feature', 'Glass', 'Watch Movement Country', "Watch's water resistance", 'compatible_with', 'os_compatibility', 'Name', 'Name in English language', 'Product Description', 'English description', 'Highlights', 'English highlights', 'Dangerous Goods', 'Video URL', 'Warranty Period', 'Warranty Policy', 'Warranty Policy EN', 'Warranty Type', 'Price', 'Special Price', 'Start date of promotion', 'End date of promotion', 'SellerSKU', 'AssociatedSku', 'Quantity', "What's in the box", 'Package Length (cm)', 'Package Width (cm)', 'Package Height (cm)', 'Package Weight (kg)', 'Free Items', 'MainImage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Color thumbnail', 'Left lens astigmatism power', 'Left lens power', 'Right lens astigmatism power', 'Right lens power', 'Lens Color', 'Frame Color', 'Eyewear size', 'Bracelet Size', 'Chain Size', 'Ring Size', 'Weight of precious metal', 'Bangle Size', 'Watch Strap Color']}

    #取前四字符
    try:
        if dic['大类'].find('TV')!=-1:
            namelist=namedic['TV, ']
        else:
            namelist=namedic[dic['大类'][0:4]]
    except:
        print('找不到对应的输出表格')
    dic['大类']=dic['大类'].replace('/','_')
    outlist=[]
    for i in namelist:
        if DorL=='a':
            try:
                outlist.append(dic[i[:5]])
            except:
                try:
                    outlist.append(dic[i])
                except:
                    outlist.append('')
        else:
            try:
                outlist.append(dic[i])
            except:
                outlist.append('')
    try:
        if not os.path.exists(str(name)+dic['大类']+'输出.csv'):
            file=open(str(name)+dic['大类']+'输出.csv','w',newline='',errors='ignore')
            csv_writer = csv.writer(file)
            csv_writer.writerow(namelist)
        else:
            file=open(str(name)+dic['大类']+'输出.csv','a',newline='',errors='ignore')
            csv_writer = csv.writer(file)
    except:
        if not os.path.exists(str(name)+dic['大类']+'输出.csv'):
            print('输出文件无法建立')
        else:
            print('输出文件无法打开，请不要在程序运行时打开输出文件')
    try:
        csv_writer.writerow(outlist)
    except:
        print('无法输出数据')
    file.close()


#爬取aliexpress页面，最重要的函数
def creepage_a(driver,name):
    

    #单个sku储存在字典里
    dic={}
    
    ##爬取和处理大类
    #定位到大类位置
    try:
        dic['大类']=driver.find_elements_by_xpath\
            ("//div[@class='breadcrumb']//a")[2].text
    except:
        dic['大类']=''
    for i in range(100):
        if len(dic['大类'])>0:
            break
        try:
            dic['大类']=driver.find_elements_by_xpath\
                ("//div[@class='breadcrumb']//a")[2].text
        except:pass
        time.sleep(0.1)
    #aliexpress到daraz的转换字典
    transdic={'Food':'Groceries','Home Appliances':'Home Appliances','Computer & Office':'Computers & Laptops','Home Improvement':'Home Appliances','Home & Garden':'Kitchen & Dining','Sports & Entertainment':'Sports & Outdoors','Education & Office Supplies':'Stationery & Craft','Toys & Hobbies':'Toys & Games','Security & Protection':'Tools, DIY & Outdoor','Automobiles & Motorcycles':'Motors','Lights & Lighting':'Furniture & Décor','Consumer Electronics':'TV, Audio _ Video, Gaming & Wearables','Beauty & Health':'Health & Beauty','Shoes':'Fashion','Electronic Components & Supplies':'Computers & Laptops','Cellphones & Telecommunications':'Mobiles & Tablets','Tools':'Tools, DIY & Outdoor','Mother & Kids':'Mother & Baby','Furniture':'Furniture & Décor','Jewelry & Accessories':'Watches Sunglasses Jewellery','Watches':'Watches Sunglasses Jewellery','Luggage & Bags':'Bags and Travel','Hair Extensions & Wigs':'Health & Beauty','Novelty & Special Use':'Tools, DIY & Outdoor','Weddings & Events':'Fashion',"Women's Clothing":'Fashion',"Men's Clothing":'Fashion','Apparel Accessories':'Fashion','Underwear & Sleepwears':'Fashion'}    
    #转换大类名称
    try:
        dic['大类']=transdic[dic['大类']]
    except:
        dic['大类']='Test'
        
        
    #点开description
    driver.find_elements_by_class_name\
        ('tab-inner-text')[4].click()
    time.sleep(1)
    
    
    #取消勾选color和type并检验其存在
    for i in range(100):
        if len(driver.find_elements_by_class_name('selected'))==0:
            break
        try:
            driver.find_element_by_class_name('selected').click()
        except:pass
        time.sleep(0.1)
    
    
    colorlist=driver.find_elements_by_class_name("sku-property-image")
    typelist=driver.find_elements_by_class_name("sku-property-text")
    
    #解决两行都是文字选项的页面
    #首先确认有几行
    sku_property_list=driver.find_elements_by_class_name("sku-property-list")
    #如果有两行且没有图像
    if len(sku_property_list)==2 and len(colorlist)==0:
        colorlist=sku_property_list[0].find_elements_by_class_name("sku-property-text")
        typelist=sku_property_list[1].find_elements_by_class_name("sku-property-text")
    
        
    #如果为空list
    if len(colorlist)==0:
        colorlist=['']
    if len(typelist)==0:
        typelist=['']
    
    
    ##开始整合爬取数据
    
    for i in range(len(colorlist)):
        #画廊的图片切换定位
        if i==0:
            try:
                picturetargetlist=driver.find_elements_by_class_name\
                    ("images-view-item")
                #建立图片列表
                picturelist=[]
                for target in picturetargetlist:
                    #移动鼠标从而换动图片
                    ActionChains(driver).move_to_element(target).perform()
                    #记录图片地址
                    picturelist.append(driver.find_element_by_class_name(\
                    'magnifier-image').get_attribute('src'))
            except:
                pass
        
        
        #如果有颜色则令颜色的图片为mainImage   
        if colorlist[i]!='':
            if colorlist[i].find_element_by_xpath("./..").\
                    get_attribute('class') == 'sku-property-item disabled':
                continue
            #写入颜色
            colorname=colorlist[i].find_element_by_xpath("./*")\
                .get_attribute('title')
            dic['Color Family']=colorname
            try:
                #点击相应颜色从而获得相应的图片
                
                colorlist[i].click()
                if i==0:
                    picturelist=[driver.find_element_by_class_name\
                        ('magnifier-image').get_attribute('src')]\
                        +picturelist
                else:
                    picturelist[0]=driver.find_element_by_class_name\
                        ('magnifier-image').get_attribute('src')
            except:
                pass
        
        #剔除重复项
        picturelist=sorted(set(picturelist),key=picturelist.index)
        
        
        #将图片放入对应槽里
        tablelist=['MainImage','Image2','Image3','Image4','Image5','Image6',\
                   'Image7','Image8',]
        #初始化
        for j in range(len(tablelist)):
            dic[tablelist[j]]=''
        #逐个写入
        for j in range(len(picturelist)):
            dic[tablelist[j]]=picturelist[j]
            
        
        for j in range(len(typelist)):
            if typelist[j]!='':
                if typelist[j].find_element_by_xpath("./..").\
                    get_attribute('class') == 'sku-property-item disabled':
                    continue
            if typelist[j]!='':
                typename=typelist[j].find_element_by_xpath\
                    ("./../../../div[1]").text
                typename=typename[:typename.find(':')]
                try:
                    dic['Color Family']=colorname+' - '+typelist[j].text
                except:
                    pass
                try:
                    typelist[j].click()
                except:
                    continue


            #爬取名称
            dic['Name']=driver.find_element_by_class_name\
                ("product-title-text").text
            
                
            ##价格计算部分
            #价格
            priceGetSuccess=0
            printerr=0
            for i in range(100):
                if priceGetSuccess==1:
                    break
                time.sleep(0.1)
                try:
                    price=driver.find_element_by_class_name\
                            ("product-price-value").text
                except:
                    price=driver.find_element_by_class_name\
                            ("uniform-banner-box-price").text
                try:
                    if price.find('-')!=-1:
                        priceGetSuccess=0
                        if printerr==0:
                            #print('警告，当前没有找到对应的价格，请手动点击')
                            printerr=1
                    else:
                        price=float(price[price.find('$')+1:price.find('.')+3])
                        priceGetSuccess=1
                except:
                    if printerr==0:
                        #print('警告，当前没有找到对应的价格，请手动点击')
                        printerr=1

            #运费
            try:
                shipping=driver.find_element_by_class_name\
                    ("dynamic-shipping-titleLayout").text
                
            except:
                shipping=driver.find_element_by_class_name\
                    ("product-shipping-price").text
            
            if shipping.find('$')!=-1:
                shipping=float(shipping[shipping.find('$')+1:])
            else:
                shipping=0
            #汇率
            exchange_rate=200
            #计算商品最终价格
            #利润率
            income=1.4
            try:
                
                
                price=round((price+shipping)*exchange_rate*income)
                #用逗号分割
                dic['Price']="{:,}".format(price)
            except:
                break
            

            try:
                dic['Product Description']
            except:
                #爬取warranty
                #try:
                #    dic['Warranty Type']=driver.find_element_by_class_name\
                #    ("product-warranty").text
                #    dic['Warranty Period']=''.\
                #        join(list(filter(str.isdigit,dic['Warranty Type'])))
                #except:
                dic['Warranty Period']='N/A'
                dic['Warranty Type']='No Warranty'
                
                ##爬取description

                desc=''
                #点开description
                driver.find_elements_by_class_name\
                            ('tab-inner-text')[4].click()
                for i in range(100):
                    if len(desc)>0:
                        break
                    try:
                        
                        desc=driver.find_element_by_class_name\
                            ('product-description').get_attribute("innerHTML")
                    except:pass
                    time.sleep(0.1)
                #进行剪裁   
                try:
                    desc=desc[:desc.find('<div class="detailmodule_dynamic">')]\
                        +desc[desc.find('</kse:widget></div>')+\
                              len('</kse:widget></div>'):]
                except:pass
                #进行替换
                try:
                    desc=desc.replace('src="//ae01','src="https://ae01')
                except:pass
                #删除js
                try:
                    desc=desc[:desc.find('<script>')]
                except:pass
                if desc=='':
                    desc='<br>'
                dic['Product Description']=desc
                
                
                
                #爬取specification
                
                targetlist=driver.find_elements_by_class_name('property-title')
                targetlist2=driver.find_elements_by_class_name('property-desc')
                
                #点开SPECIFICATIONS
                driver.find_elements_by_class_name\
                    ('tab-inner-text')[6].click()
                    
                for i in range(100):
                    if len(targetlist)!=0 and len(targetlist2)!=0:
                        break
                    targetlist=driver.find_elements_by_class_name('property-title')
                    targetlist2=driver.find_elements_by_class_name('property-desc')
                    time.sleep(0.1)
                #一个是key，一个是value
                #暂时不用specification
                for p in range(len(targetlist2)):
                    #dic[targetlist[p].text]=targetlist2[p].text
                    pass

                ##爬取highlight
                #aliexpress没有highlight,使用specification的文本代替
                try:
                    dic['Highlights']=driver.\
                    find_element_by_class_name('product-specs-list')\
                    .get_attribute("innerHTML")
                    
                    #dic['Highlights']='<ul>\n <li>'+driver.\
                    #find_element_by_class_name('product-specs-list').text\
                    #.replace('\n','</li>\n <li>')+'</li>\n</ul>'
                except:
                    dic['Highlights']='<br>' 
                    
            #设置SKU
            global SKU
            global SKUtitle
            #SKU的格式
            dic['SellerSKU']=SKUtitle+("-{:0>9d}".format(SKU))
            #只有第一个被设置为主SKU
            if i==0 and j==0:
                mainSKU=dic['SellerSKU']
            try:
                dic['AssociatedSku']=mainSKU
            #如果i=0，j=0的情况被跳过了
            except:
                mainSKU=dic['SellerSKU']
                dic['AssociatedSku']=mainSKU
            #数字+1
            SKU+=1
            
            #爬取what is in box


            #aliexpress没有highlight

            dic['Package Length (cm)']=10
            dic['Package Width (cm)']=10
            dic['Package Height (cm)']=10
            dic['Package Weight (kg)']=0.3
            dic['Quantity']=999
            
            #设置英文
            dic['Name in English language']=dic['Name']
            dic['English description']=dic['Product Description']
            dic['English highlights']=dic['Highlights']
            dic["What's in the box"]='1'
            

            #尝试输出
            try:
                output(dic,name)
            except:
                print(dic['Name']+'输出错误(output error)')
            if typelist[j]!='':
                #恢复原样
                typelist[j].click()



#爬取页面，最重要的函数
def creepage(driver,name):
    #对付烦人的Ships from overseas
    try:
        time.sleep(0.02)
        driver.find_element_by_class_name('sfo__close').click()
    except:
        pass
    #单个sku储存在字典里
    dic={}
    dic['大类']=driver.find_elements_by_class_name("breadcrumb_item_text")[0].text
    #lazada到daraz的转换字典
    transdic={'Audio':'TV, Audio _ Video, Gaming & Wearables','Bags and Travel':'Bags and Travel','Beauty':'Health & Beauty','Bedding & Bath':'Bedding & Bath','Cameras & Drones':'Cameras','Computers & Laptops':'Computers & Laptops','Data Storage':'Computers & Laptops','Digital Goods':'Digital Goods','Digital Utilities':'Digital Goods','Electronics Accessories':'Computers & Laptops','Free Sample (Flexi Combo)':'Sample','Furniture & Organization':'Furniture & Décor','Groceries':'Groceries','Health':'Health & Beauty','Household Supplies':'Home Appliances','Kitchen & Dining':'Kitchen & Dining','Large Appliances':'Home Appliances','Laundry & Cleaning Equipment':'Laundry & Cleaning','Lighting & Décor':'Furniture & Décor','Media, Music & Books':'Media, Music & Books',"Men's Shoes and Clothing":'Fashion','Mobiles & Tablets':'Mobiles & Tablets','Monitors & Printers':'Computers & Laptops','Mother & Baby':'Mother & Baby','Motors':'Motors','Outdoor & Garden':'Tools, DIY & Outdoor','Pet Supplies':'Pet Supplies','Service Product':'Service Product','Services':'Service Product','Small Appliances':'Home Appliances','Smart Devices':'Tools, DIY & Outdoor','Special Digital Products':'Digital Goods','Sports & Outdoors':'Sports & Outdoors','Sports Shoes and Clothing':'Fashion','Stationery & Craft':'Tools, DIY & Outdoor','Surprise Box':'Sample','Televisions & Videos':'TV, Audio _ Video, Gaming & Wearables','Tools & Home Improvement':'Tools, DIY & Outdoor','Toys & Games':'Toys & Games','Watches Sunglasses Jewellery':'Watches Sunglasses Jewellery',"Women's Shoes and Clothing":'Fashion'}
    #转换大类名称
    try:
        if DorL=='l':
            dic['大类']=transdic[dic['大类']]
    except:
        print('转换失败，lazada商品难以并入daraz表格')
    #首先要爬取color与style，这样才能组合出SKU
    #取消勾选color和type并检验其存在
    #对付烦人的Ships from overseas
    try:
        time.sleep(0.02)
        driver.find_element_by_class_name('sfo__close').click()
    except:
        pass
    try:#定位被选中的color图片
        driver.find_element_by_class_name("sku-variable-img-wrap-selected").click()
        WebDriverWait(driver,10,0.1).until_not(lambda x:\
            x.find_element_by_class_name("sku-variable-img-wrap-selected"))
        color=1
    except:
        color=0
        
    try:#定位被选中的style
        driver.find_element_by_class_name("sku-variable-name-selected").click()
        WebDriverWait(driver,10,0.1).until_not(lambda x:\
            x.find_element_by_class_name("sku-variable-name-selected"))
        type=1
    except:
        try:#定位被选中的style
            driver.find_element_by_class_name("sku-variable-size-selected").click()
            WebDriverWait(driver,10,0.1).until_not(lambda x:\
               x.find_element_by_class_name("sku-variable-size-selected"))
            type=1
        except:
            type=0
    
    #爬取所有color
    colorlist=[]#创立color列表
    if color==1:
        #找到所有color
        corlortargetlist=driver.find_elements_by_class_name("sku-variable-img-wrap")
        for target in corlortargetlist:
            ActionChains(driver).move_to_element(target).perform()
            colorlist.append(driver.find_element_by_class_name\
                             ("sku-name-hover").text)
    else:
        colorlist.append('')
        
    #爬取所有type
    typelist=[]#创立type列表
    if type==1:
        typeName=driver.find_elements_by_class_name("sku-prop-selection")[-1].text\
        .splitlines()[0]#获得type的名字
        #找到所有type
        try:
            driver.find_element_by_class_name("sku-variable-name")
            typetargetlist=driver.find_elements_by_class_name("sku-variable-name")
        except:
            pass
        try:
            driver.find_element_by_class_name("sku-variable-size")
            typetargetlist=driver.find_elements_by_class_name("sku-variable-size")
        except:
            pass
        for target in typetargetlist:
            ActionChains(driver).move_to_element(target).perform()
            typelist.append(driver.find_element_by_class_name\
                            ("sku-name-hover").text)
    else:
        typeName=''
        typelist.append('')
    #对付烦人的Ships from overseas
    try:
        time.sleep(0.02)
        driver.find_element_by_class_name('sfo__close').click()
    except:
        pass
    #点开view more
    driver.execute_script('window.scrollBy(0,200)')
    try:
        driver.find_element_by_class_name('pdp-view-more-btn').click()
        time.sleep(0.01)
        #还原位置
        driver.execute_script('window.scrollBy(0,-9999)')
    except:
        pass
    #对付烦人的Ships from overseas
    try:
        time.sleep(0.02)
        driver.find_element_by_class_name('sfo__close').click()
    except:
        pass
    #开始整合数据
    for i in range(len(colorlist)):
        if color==1:
            corlortargetlist[i].click()#点击相应颜色
            #点击相应款式，从而获得相应的图片
            try:
                driver.find_element_by_class_name('sku-variable-name').click()
            except:
                pass
            try:
                driver.find_element_by_class_name('sku-variable-size').click()
            except:
                pass
        #画廊的图片切换定位
        try:
            picturetargetlist=driver.find_elements_by_class_name\
                ("item-gallery__image-wrapper")
            #建立图片列表
            picturelist=[]
            for target in picturetargetlist:
                #移动鼠标从而换动图片
                ActionChains(driver).move_to_element(target).perform()
                WebDriverWait(driver,10,0.1).until(lambda x:\
                x.find_element_by_class_name("gallery-preview-panel__image"))
                #记录图片地址
                picturelist.append(driver.find_element_by_class_name(\
                'gallery-preview-panel__image').get_attribute('src'))
        except:
            pass
        
        #剔除重复项
        picturelist=sorted(set(picturelist),key=picturelist.index)
        
        #将图片放入对应槽里
        tablelist=['MainImage','Image2','Image3','Image4','Image5','Image6','Image7','Image8',]
        #初始化
        for j in range(len(tablelist)):
            dic[tablelist[j]]=''
        #逐个写入
        for j in range(len(picturelist)):
            dic[tablelist[j]]=picturelist[j]
            
        #恢复样式状态
        try:
            driver.find_element_by_class_name('sku-variable-name-selected').click()
        except:
            pass
        #恢复样式状态
        try:
            driver.find_element_by_class_name('sku-variable-size-selected').click()
        except:
            pass
        #写入颜色
        dic['Color Family']=colorlist[i]
        for j in range(len(typelist)):
            if typeName!='':
                dic['typeName']=typelist[j]
                dic['Color Family']=colorlist[i]+' - '+typelist[j]
                typetargetlist[j].click()
                time.sleep(0.1)
            #爬取名称和价格
            dic['Name']=driver.find_element_by_class_name("pdp-mod-product-badge-title").text

            pricelist=driver.find_elements_by_class_name("pdp-price")
            if len(pricelist)==1:
                dic['Price']=pricelist[0].text
            else:
                dic['Price']=pricelist[1].text
                dic['Special Price']=pricelist[0].text
            
                
            #爬取warranty
            try:
                dic['Warranty Type']=driver.find_element_by_class_name\
                ("delivery-option-item_type_warranty").text
                dic['Warranty Period']=''.join(list(filter(str.isdigit,dic['Warranty Type'])))
            except:
                dic['Warranty Period']='N/A'
                dic['Warranty Type']='No Warranty'
            
            #爬取highlight
            try:
                dic['Highlights']='<ul>\n <li>'+driver.find_element_by_class_name(\
                "pdp-product-highlights").text.replace('\n','</li>\n <li>')+'</li>\n</ul>'
            except:
                pass
            
            #爬取description
            desc=''
            for i in range(1000):
                if len(desc)>0:
                    break
                try:
                    desc=driver.find_element_by_class_name\
                            ('detail-content').get_attribute("innerHTML")
                except:pass
                time.sleep(0.1)


            if desc=='':
                desc='<br>'
            dic['Product Description']=desc
            

            #爬取specification
            try:
                targetlist=driver.find_elements_by_class_name('key-title')
                targetlist2=driver.find_elements_by_class_name('key-value')
                for p in range(len(targetlist2)):
                    dic[targetlist[p].text]=targetlist2[p].text

            except:pass
            
            #设置SKU
            global SKU
            global SKUtitle
            #SKU的格式
            dic['SellerSKU']=SKUtitle+("-{:0>9d}".format(SKU))
            #只有第一个被设置为主SKU
            if i==0 and j==0:
                mainSKU=dic['SellerSKU']
            try:
                dic['AssociatedSku']=mainSKU
            #如果i=0，j=0的情况被跳过了
            except:
                mainSKU=dic['SellerSKU']
                dic['AssociatedSku']=mainSKU
            #数字+1
            SKU+=1
            
            
            try:
                dic["What's in the box"]=driver.find_element_by_class_name\
                ('box-content-html').text
            except:
                pass
                #print(dic['Name']+'没有what is in box')
            dic['Package Length (cm)']=10
            dic['Package Width (cm)']=10
            dic['Package Height (cm)']=10
            dic['Package Weight (kg)']=0.3
            dic['Quantity']=999



            #设置英文
            dic['Name in English language']=dic['Name']
            dic['English description']=dic['Product Description']
            dic['English highlights']=dic['Highlights']
            if len(dic["What's in the box"])==0:
                dic["What's in the box"]='1'



            try:
                output(dic,name)
            except:
                print(dic['Name']+'输出错误(output error)')
            if typeName!='':
                #恢复原样
                typetargetlist[j].click()

#只爬一页
def creepone(url,name):
    #此处代码能够在加载前找到元素
    DesiredCapabilities.CHROME["pageLoadStrategy"] = "eager"
    #driver=webdriver.Chrome(desired_capabilities=capa)
    driver=set_spider_option("chromedriver.exe")
    driver.get(url)
    #try:
    if DorL=='a':
        add_cookie(driver,url)
        creepage_a(driver,name)
    else:
        creepage(driver,name)
    #except:
    #    print('creepage error')
    driver.close()
    
#获得aliexpress商品链接
def getlist_a(driver,p):
    #获得所有商品链接位置
    container=driver.find_element_by_class_name("product-container")
    product=container.find_elements_by_xpath("./*/a")
    #获得标签图片位置
    #darazmall=driver.find_elements_by_class_name("c3vCyH")
    #商品链接列表
    productlist=[]
    for i in range(len(product)):
        #去除带商标的
        if p==0:
            try:
                productlist.append(product[i].get_attribute('href'))
                #darazmall[i].find_element_by_class_name\
                        #('ic-dynamic-badge-lazMall')
            except:
                productlist.append(product[i].get_attribute('href'))
        else:
            productlist.append(product[i].get_attribute('href'))
    return(productlist)
    
#获得商品链接
def getlist(driver,p):
    #获得所有商品链接位置
    if DorL=='d':
        product=driver.find_elements_by_xpath("//div[@class='c16H9d']//a[1]")
    elif DorL=='l':
        product=driver.find_elements_by_xpath("//div[@class='RfADt']//a[1]")
    #获得daraz标签图片位置
    if DorL=='d':
        darazmall=driver.find_elements_by_class_name("c3vCyH")
    elif DorL=='l':
        darazmall=driver.find_elements_by_class_name("RfADt")
    #商品链接列表
    productlist=[]
    for i in range(len(product)):
        if p==0:
            try:
                darazmall[i].find_element_by_class_name\
                        ('ic-dynamic-badge-lazMall')
            except:
                productlist.append(product[i].get_attribute('href'))
        else:
            productlist.append(product[i].get_attribute('href'))
    return(productlist)
#暂停
def pause(page):
    if keyboard.is_pressed('p'):
        try:
            print('当前在第'+str(page)+'页')
        except:
            pass
        #按q再开始
        keyboard.wait('q')
        

#获得当前页数
def getpage(url):
    page=url.find('page=')
    if page==-1:
        url=url+'&page=2'
        page=1
    elif url[url.find('page=')+5:].find('&')==-1:
        page=url[url.find('page=')+5:]
    else:
        page=url[url.find('page=')+5:][:url[url.find('page=')+5:].find('&')]
    #print('当前在第'+page+'页')
    return page

#返回下一页的网址
def nextpage(url):
    page=url.find('page=')
    if page==-1:
        url=url+'&page=2'
    elif url[url.find('page=')+5:].find('&')==-1:
        page=url[url.find('page=')+5:]
        url=url[:url.find('page=')+5]+str(int(page)+1)
    else:
        page=url[url.find('page=')+5:][:url[url.find('page=')+5:].find('&')]
        rest=url[url.find('page=')+5:][url[url.find('page=')+5:].find('&'):]
        url=url[:url.find('page=')+5]+str(int(page)+1)+rest
    return url
#爬取aliexpress整个列表
def creepall_a(url,p,name,page):

    #此处代码能够在加载前找到元素
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "eager"
    driver=set_spider_option("chromedriver.exe")
    #driver.implicitly_wait(60)
    #设置如何结束
    end_creep=0
    driver.get(url)
    if driver.current_url.find('error')!=-1:
        driver.get(url)
    #driver.find_element_by_class_name('footer-copywrite')
    #初始化页面网址
    while(1):
        try:
            driver.execute_script('window.scrollBy(0,100)')
            time.sleep(0.05)
            driver.find_element_by_class_name('next-next').click()
            url=driver.current_url
            rest=url[url.find('page=')+6:][url[url.find('page=')+6:].find('&'):]
            url=url[:url.find('page=')+5]+'1'+rest
            driver.get(url)
            if driver.current_url.find('error')!=-1:
                driver.get(url)
            break
        except:pass
    
    #driver.find_element_by_class_name('next-prev').click()
    
    #获得当前网址
    url=driver.current_url
    #如果指定页不是第一页，则跳转
    if page!='' and page!='1':
        rest=url[url.find('page=')+6:][url[url.find('page=')+6:].find('&'):]
        url=url[:url.find('page=')+5]+page+rest
        driver.get(url)
        if driver.current_url.find('error')!=-1:
            driver.get(url)
    
    for i in range(100):
        driver.execute_script('window.scrollBy(0,100)')
        time.sleep(0.05)
    #得到商品链接
    productlist=getlist_a(driver,p)
    #k代表当前页面的第几个商品
    k=0
    page=getpage(url)
    print('当前在第'+str(int(page))+'页')
    while(1):
    
        #得到所有商品的链接位置
        if k>=len(productlist):
            
            url=nextpage(url)
            page=getpage(url)
            print('当前在第'+str(int(page))+'页')
            while(1):
                driver.get(url)
                if driver.current_url.find('error')!=-1:
                    driver.get(url)
                #使得加载所有的商品
                #滚个100下
                for i in range(100):
                    driver.execute_script('window.scrollBy(0,100)')
                    time.sleep(0.05)
                #得到商品链接
                try:
                    productlist=getlist_a(driver,p)
                    if len(productlist)!=0:
                        break
                except:
                    end_creep=1
                    break
            k=0
            #得到信号，结束爬虫
            if end_creep==1:
                break
        #开始爬虫
        #按p暂停
        try:
            pause(page)
        except:
            pass
        time.sleep(0.1)
        #直接切换网页
        #先加载网页，再加载cookie
        add_cookie(driver,productlist[k])
        #按p暂停
        try:
            pause(page)
        except:
            pass
        try:
            #pass
            creepage_a(driver,name)
        except:pass
            #print('creepage error')

        #按p暂停
        try:
            pause(page)
        except:
            pass
        #至此，这个商品爬虫结束了
        #关闭当前页面，返回列表
        time.sleep(0.1)
        k+=1
    driver.close()

#爬取整个列表
def creepall(url,p,name):

        #此处代码能够在加载前找到元素
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "eager"
        #driver=webdriver.Chrome(desired_capabilities=capa)
        driver=set_spider_option("chromedriver.exe")
        #driver.implicitly_wait(60)
        driver.get(url)
        #等待元素加载完毕
        for i in range(20):
            driver.execute_script('window.scrollBy(0,400)')
            time.sleep(0.01)
        #得到商品链接
        productlist=getlist(driver,p)
        time.sleep(0.5)
        
        
        page=getpage(url)
        print('当前在第'+str(int(page))+'页')
        while(1):
            
            #得到所有商品的链接位置
            
            if len(productlist)==0:
            
                url=nextpage(url)
                page=getpage(url)
                print('当前在第'+str(int(page))+'页')
                driver.get(url)
                #等待元素加载完毕
                for i in range(20):
                    driver.execute_script('window.scrollBy(0,400)')
                    time.sleep(0.01)    

                #得到商品链接
                try:
                    productlist=getlist(driver,p)
                except:
                    break
                
                
            #开始爬虫
            #按p暂停
            try:
                pause(page)
            except:
                pass
            
            time.sleep(0.1)
            #直接切换网页
            try:
                driver.get(productlist[0])
            except:
                pass
            
            #按p暂停
            try:
                pause(page)
            except:
                pass

            try:
                creepage(driver,name)
            except:
                #print('creepage error')
                pass

            #按p暂停
            try:
                pause(page)
            except:
                pass
            
            #至此，这个商品爬虫结束了
            #关闭当前页面，返回列表

            time.sleep(0.1)

            productlist=productlist[1:]
        driver.close()
#erp转换
def trans(erp,store,table):
    wb=xlrd.open_workbook(erp)
    
    #按工作簿定位工作表
    sh=wb.sheet_by_index(0)
    outdic={'主sku编号':'初始化占位符'}
    for i in range(sh.nrows-1):
    #将数据和标题组合成字典
        dic=dict(zip(sh.row_values(0),sh.row_values(i+1)))
        dic['大类']=table
        if dic['主sku编号']!=outdic['主sku编号']:
            outdic={}
            outdic['主sku编号']=dic['主sku编号']
            outdic['Name']=dic['产品英文名']
            outdic['Brand']=dic['品牌']
            outdic['Color Family']=dic['属性值']
            outdic['Product Description']=dic['纯文本描述']
            outdic['Highlights']=dic['Bullet Point']
            outdic['MainImage']=dic['产品主图']
            outdic['Image2']=dic['子sku多属性图片']
        else:
            outdic['Image2']=dic['子sku多属性图片']
            outdic['Color Family']=dic['属性值']
        dic['Package Length (cm)']=10
        dic['Package Width (cm)']=10
        dic['Package Height (cm)']=10
        dic['Package Weight (kg)']=0.3
        dic['Quantity']=999
        
        output(outdic,table)

#爬虫设置与分配引流
def creepset(url,page,name,p,SKUnumber,SKUt):
    #设置初始SKU
    global SKU
    global SKUtitle
    if len(SKUt)>0:
        SKUtitle=SKUt
    try:
        SKU=int(SKUnumber)
    except:
        if SKUnumber=='':
            print('检测到SKU输入为空，默认从1开始')
        else:
            print('请输入正整数')
    #设置是daraz还是lazada还是aliexpress
    try:
        global DorL
        if url.find('lazada')!=-1:
            DorL='l'
        elif url.find('aliexpress')!=-1:
            DorL='a'
        else:
            DorL='d'
    except:
        pass
    if page=='':
        page=1
    try:
        if DorL=='a':
            page=str(page)
            if url.find('item')!=-1:
                #启动新线程
                _thread.start_new_thread(creepone,(url,name))
            else:
                #启动新线程
                _thread.start_new_thread(creepall_a,(url,p,name,page))
        elif url.find('products')!=-1:
            _thread.start_new_thread(creepone,(url,name))
            #creepone(url)
        else:
            pageget=getpage(url)
            if pageget==1:
                url=url+'&page='+str(page)
            else:
                url=url.replace(pageget,page)
            _thread.start_new_thread(creepall,(url,p,name))
            #creepall(url,p)
    except:
        print('线程启动失败')

#文件选择框
def selectPath(E):
    #选择文件path_接收文件地址
    path_ = tkinter.filedialog.askopenfilename()
    E.insert(0,path_)

#主程序
def main():
    
    #主程序部分
    top = tkinter.Tk()
    top.title('爬取 版本1.53')


    #文字
    tkinter.Label(top,text="粘贴爬取的列表或商品网址").grid(row=2, column=0)
    tkinter.Label(top,text="从第几页开始").grid(row=3, column=0)
    tkinter.Label(top,text="输出表格名称").grid(row=4, column=0)
    tkinter.Label(top,text="设置初始SKU数字，不填默认为1")\
    .grid(row=5, column=0)
    tkinter.Label(top,text="设置SKU前缀，不填默认为A").grid(row=6, column=0)
    tkinter.Label(top,text="按住p暂停，再按q开始").grid(row=7, column=0)
    tkinter.Label(top,text="爬取时请关闭excel，否则无法输出").grid(row=8, column=0)
    
    
    tkinter.Label(top,text="\n").grid(row=10, column=0)
    tkinter.Label(top,text="erp类别(爬虫不用选这个)").grid(row=11, column=0)
    tkinter.Label(top,text="erp表位置").grid(row=12, column=0)
    tkinter.Label(top,text="库存表位置").grid(row=13, column=0)
    
    #输入框
    E1=tkinter.Entry(top,bd=1)
    E1.grid(row=2,column=3)
    E2=tkinter.Entry(top,bd=1)
    E2.grid(row=3,column=3)
    E3=tkinter.Entry(top,bd=1)
    E3.grid(row=4,column=3)
    E99=tkinter.Entry(top,bd=1)
    E99.grid(row=5,column=3)
    E98=tkinter.Entry(top,bd=1)
    E98.grid(row=6,column=3)
    E5=tkinter.Entry(top,bd=1)
    E5.grid(row=12,column=3)
    E6=tkinter.Entry(top,bd=1)
    E6.grid(row=13,column=3)
    
    #下拉菜单
    cbox=ttk.Combobox(top)
    cbox.grid(row=11,column=3)
    cbox['value']=('Bags and Travel', 'Bedding & Bath', 'Cameras', 'Charity and Donation','Computers & Laptops', 'Digital Goods', 'Fashion', 'Furniture & Décor','Groceries', 'Health & Beauty', 'Home Appliances', 'Kitchen & Dining','Laundry & Cleaning', 'Livestock', 'Media, Music & Books', 'Mobiles & Tablets','Mother & Baby', 'Motors', 'OPS Services', 'Packaging Material', 'Pet Supplies','Sample', 'Service Product', 'Sports & Outdoors', 'Stationery & Craft', 'Test Product2','Tools, DIY & Outdoor', 'Toys & Games', 'TV, Audio _ Video, Gaming & Wearables','Watches Sunglasses Jewellery')
    
    #勾选框
    cv1=tkinter.IntVar()
    C1=tkinter.Checkbutton(top,text="包括带商标的",variable=cv1,onvalue=1,\
                           offvalue=0)
    C1.grid(row=7, column=3)


    #按钮    
    tkinter.Button(top, text ="爬取",command=lambda:creepset\
                   (E1.get(),E2.get(),E3.get(),cv1.get(),E99.get(),E98.get()))\
        .grid(row=3, column=5)

        
    tkinter.Button(top, text ="选择",command=lambda:selectPath(E5)).grid(row=12, column=4)
    tkinter.Button(top, text ="erp转换",command=lambda:\
                   trans(E5.get(),E6.get(),cbox.get())).grid(row=12, column=5)
    tkinter.Button(top, text ="选择",command=lambda:selectPath(E6)).grid(row=13, column=4)
    
    top.mainloop()

code=input()
if code=='20220311':
    main()

#以下是测试
#url='https://www.daraz.pk/catalog/?q=phone+case&_keyori=ss&from=input&spm=a2a0e.searchlist.search.go.474648a0C5kbem&page=2'
#name=''
#creepall(url,0,name)