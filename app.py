import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatMemberUpdated
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
import openai
import random

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Replace these with your actual keys
TELEGRAM_BOT_TOKEN = "7846804361:AAHSTz20bVshGiMhO9uXyoI0tlBpdGaSdxw"
OPENAI_API_KEY = "sk-svcacct-6KTY_iNm2MbgNpwCVH2Q9-_XrEYQ8IgOggD9LhDny-Yg5cc5S5RCrAbdY2ZHU0fWOT3BlbkFJ43JV0cOYk4m0fvCxyBUAidHRBx2NHuMUg9Jxq_h5Ik6-gz-zMEA1pF6ajxHTil97QA"

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()  # Create a router for handling commands and messages

# Categories: Facts, Quotes, Billionaires
facts = [
    "The top 1% of earners globally own more than 40% of the world’s wealth.",
    "There are over 2,600 billionaires in the world today.",
    "The richest 10% of the global population owns 76% of the world’s wealth.",
    "Elon Musk became the richest person in the world in 2021 due to Tesla's soaring stock prices.",
    "Warren Buffett bought his first stock at age 11 and filed his first tax return at age 13.",
    "Jeff Bezos started Amazon as an online bookstore in 1994 from his garage.",
    "Bernard Arnault’s LVMH is the largest luxury goods company in the world.",
    "Bill Gates has donated over $50 billion to charitable causes through the Gates Foundation.",
    "Mark Zuckerberg became a billionaire at the age of 23, making him one of the youngest self-made billionaires in history.",
    "Oprah Winfrey was born into poverty but became the first African American female billionaire.",
    "The world's first billionaire was John D. Rockefeller, in 1916.",
    "In 2023, the top five wealthiest individuals collectively held over $800 billion in wealth.",
    "China has the most self-made female billionaires in the world.",
    "The most common industry for billionaires is finance and investments.",
    "The wealthiest 20% of Americans own 88% of the country's wealth.",
    "Bill Gates founded Microsoft in 1975 with Paul Allen, revolutionizing the software industry.",
    "Amazon started as a bookstore but later expanded into a global e-commerce and technology empire.",
    "Tesla's Model 3 is one of the best-selling electric vehicles globally.",
    "The United States has the highest number of billionaires, followed by China.",
    "LVMH owns more than 70 luxury brands, including Louis Vuitton, Moët & Chandon, and Christian Dior.",
    "Warren Buffett's Berkshire Hathaway has holdings in diverse sectors, including insurance, energy, and food.",
    "The top 10 richest people in the world have more combined wealth than the entire GDP of some countries.",
    "Mark Zuckerberg co-founded Facebook in 2004, which eventually grew into Meta Platforms, a tech giant.",
    "Jack Ma built Alibaba from a small start-up into one of the world's largest e-commerce companies.",
    "The world's biggest private employer is Walmart, employing over 2.3 million people globally.",
    "Elon Musk founded SpaceX with the goal of reducing space transportation costs and making Mars colonization possible.",
    "Facebook has more than 2.8 billion active monthly users globally, making it the most popular social media platform.",
    "Tesla’s market cap exceeded $1 trillion for the first time in 2021, making it one of the most valuable car companies globally.",
    "The total value of global luxury goods sales in 2021 was estimated to be over $300 billion.",
    "Apple became the first company to reach a $2 trillion market capitalization in 2020.",
    "In 2020, Amazon’s annual revenue was over $380 billion, making it one of the largest companies in the world.",
    "Mark Zuckerberg spent $100 million to purchase the land surrounding his home to ensure privacy.",
    "Elon Musk’s company, SpaceX, was the first private company to send astronauts to the International Space Station in 2020.",
    "The wealthiest woman in the world, as of 2021, was L'Oréal heir Françoise Bettencourt Meyers.",
    "In 2021, the United States had more than 750 billionaires, the highest number of billionaires in any country.",
    "Tesla’s Gigafactories aim to produce more electric vehicles than all other manufacturers combined by 2030.",
    "Apple’s iPhone is one of the most profitable consumer products ever created, with over 2 billion units sold worldwide.",
    "The total value of all the world's real estate is estimated to exceed $280 trillion.",
    "Bill Gates owns one of the largest private landholdings in the United States, with over 242,000 acres of farmland.",
    "Google processes more than 3.5 billion searches per day, making it the most-used search engine in the world.",
    "The Amazon Rainforest is sometimes referred to as the ‘lungs of the planet’ due to its role in absorbing carbon dioxide.",
    "The world’s largest oil company is Saudi Aramco, with a market value of over $1.9 trillion.",
    "The richest person in history is thought to be Mansa Musa I of Mali, whose wealth would amount to over $400 billion today.",
    "Bitcoin reached an all-time high value of over $64,000 in April 2021.",
    "The total value of the world's stock markets exceeds $100 trillion.",
    "In 2020, the global wealth of billionaires grew by over $3.9 trillion.",
    "The average age of the world's richest billionaires is 67 years old.",
    "Apple's revenue from its App Store exceeded $64 billion in 2020.",
    "Nike is one of the most valuable sportswear brands globally, valued at over $200 billion.",
    "The top 10 most valuable brands in the world are all worth over $200 billion each.",
    "Dubai's Burj Khalifa is the tallest building in the world, standing at 828 meters (2,717 feet).",
    "The first trillion-dollar company was Apple, which reached the milestone in 2018.",
    "Billionaires saw their combined wealth increase by 27% in 2020 during the global pandemic.",
    "Tesla's electric cars have been credited with significantly accelerating the adoption of electric vehicles worldwide.",
    "The financial technology (fintech) industry has grown rapidly, with global fintech investment reaching over $100 billion in 2020.",
    "The total value of global e-commerce sales was estimated at over $5 trillion in 2021.",
    "In 2021, global luxury car sales hit a record high, surpassing 10 million units sold worldwide.",
    "In 2020, the number of active cryptocurrency wallets exceeded 50 million globally.",
    "The average salary of a top CEO in the U.S. in 2020 was over 300 times higher than the average worker's salary.",
    "China has the most billionaires globally, surpassing the United States in 2020.",
    "The combined wealth of the world’s 2,700 billionaires exceeds the GDP of the entire European Union.",
    "In 2020, the world’s total debt reached over $281 trillion, making it 355% of global GDP.",
    "In 2021, the market capitalization of the global tech industry surpassed $10 trillion.",
    "Amazon's Prime membership exceeded 200 million subscribers worldwide in 2021.",
    "In 2021, over 4.5 billion people were using social media platforms globally.",
    "The world’s largest consumer electronics company by revenue is Samsung, followed by Apple.",
    "More than 1.5 billion smartphones are sold annually worldwide.",
    "As of 2021, the global gaming industry was valued at over $159 billion.",
    "In 2020, 62% of global internet traffic was driven by mobile devices.",
    "In 2021, the value of the global cryptocurrency market surpassed $2.5 trillion.",
    "The global online video streaming industry was worth over $50 billion in 2020.",
    "More than 80% of the world’s population now has access to mobile broadband.",
    "In 2020, Google’s parent company Alphabet became the fourth company to exceed $2 trillion in market value.",
    "In 2021, the global electric vehicle market was valued at over $250 billion.",
    "The largest wealth transfer in history is expected to take place over the next two decades, transferring over $30 trillion from Baby Boomers to their heirs.",
    "The global fintech industry is expected to exceed $300 billion by 2025.",
    "Amazon’s cloud computing division, AWS, generates over $50 billion in annual revenue.",
    "Facebook’s revenue surpassed $117 billion in 2021, a 37% increase from the previous year.",
    "The video game industry is expected to reach $200 billion in revenue by 2023.",
    "The total number of billionaires globally exceeded 2,700 in 2021, with new billionaires emerging every day.",
    "The global aviation industry is worth over $900 billion, with commercial airlines flying over 4 billion passengers annually.",
    "In 2021, Tesla’s stock price increased by over 700%, making it one of the fastest-growing companies in history.",
    "The fashion industry is worth over $2.5 trillion, making it one of the largest industries in the world.",
    "In 2021, the total value of global mergers and acquisitions reached a record $5 trillion.",
    "The global insurance industry is worth over $5 trillion, with premiums exceeding $4 trillion annually.",
    "In 2020, the world’s luxury goods market contracted by 23%, but it rebounded strongly in 2021.",
    "More than 60% of global wealth is held by just 1% of the population.",
    "The global tech industry employs over 20 million people worldwide.",
    "Apple's iPhone is responsible for over 40% of the company's revenue.",
    "In 2021, the total market value of the world's top 10 tech companies exceeded $15 trillion.",
    "The total number of internet users worldwide exceeded 4.9 billion in 2021.",
    "The global travel industry was valued at over $9 trillion in 2019, with tourism being a major contributor to global GDP.",
    "In 2021, the global market for electric vehicles grew by over 100%, with sales reaching 6.5 million units.",
    "The combined wealth of the world’s top 100 richest people equals more than the GDP of Japan.",
    "In 2020, the global food delivery market was valued at over $100 billion.",
    "The global online education market is expected to reach over $350 billion by 2025.",
    "Over 90% of the world’s data has been created in the past two years.",
    "The world’s largest retail company by revenue is Walmart, followed by Amazon and Costco.",
    "In 2020, global oil consumption decreased by nearly 10% due to the COVID-19 pandemic, but it is expected to rebound in the coming years.",
    "The global clean energy sector is expected to be worth over $2 trillion by 2030.",
    "In 2021, 62% of all wealth in the United States was controlled by the top 10% of earners."
]


quotes = [
     "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
    "Don’t be afraid to give up the good to go for the great. - John D. Rockefeller",
    "I find that the harder I work, the more luck I seem to have. - Thomas Jefferson",
    "Do not wait to strike till the iron is hot, but make it hot by striking. - William Butler Yeats",
    "Wealth consists not in having great possessions, but in having few wants. - Epictetus",
    "Your income is directly related to your philosophy, not the economy. - Jim Rohn",
    "You must gain control over your money or the lack of it will forever control you. - Dave Ramsey",
    "Formal education will make you a living; self-education will make you a fortune. - Jim Rohn",
    "It’s not whether you get knocked down; it’s whether you get up. - Vince Lombardi",
    "If you really look closely, most overnight successes took a long time. - Steve Jobs",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Success is not in what you have, but who you are. - Bo Bennett",
    "Do not be embarrassed by your failures, learn from them and start again. - Richard Branson",
    "Opportunities don't happen, you create them. - Chris Grosser",
    "Don’t let the fear of losing be greater than the excitement of winning. - Robert Kiyosaki",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "You must be the change you wish to see in the world. - Mahatma Gandhi",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Hardships often prepare ordinary people for an extraordinary destiny. - C.S. Lewis",
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "You only live once, but if you do it right, once is enough. - Mae West",
    "Success is how high you bounce when you hit bottom. - George S. Patton",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Don't wait for opportunity. Create it. - Unknown",
    "Nothing will work unless you do. - Maya Angelou",
    "Dream big and dare to fail. - Norman Vaughan",
    "I am not a product of my circumstances. I am a product of my decisions. - Stephen Covey",
    "The secret of getting ahead is getting started. - Mark Twain",
    "The best way to predict the future is to create it. - Peter Drucker",
    "In order to succeed, we must first believe that we can. - Nikos Kazantzakis",
    "You don't have to be great to start, but you have to start to be great. - Zig Ziglar",
    "Do one thing every day that scares you. - Eleanor Roosevelt",
    "Don't be afraid to give up the good to go for the great. - John D. Rockefeller",
    "The journey of a thousand miles begins with one step. - Lao Tzu",
    "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "Your time is limited, so don’t waste it living someone else’s life. - Steve Jobs",
    "Act as if what you do makes a difference. It does. - William James",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "It always seems impossible until it's done. - Nelson Mandela",
    "You can't cross the sea merely by standing and staring at the water. - Rabindranath Tagore",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is the sum of small efforts, repeated day in and day out. - Robert Collier",
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    "A person who never made a mistake never tried anything new. - Albert Einstein",
    "Life is what happens when you're busy making other plans. - John Lennon",
    "Don’t count the days, make the days count. - Muhammad Ali",
    "I find that the harder I work, the more luck I seem to have. - Thomas Jefferson",
    "Failure is not the opposite of success, it is part of success. - Arianna Huffington",
    "Success is how you bounce back from failure. - Unknown",
    "Keep your face always toward the sunshine—and shadows will fall behind you. - Walt Whitman",
    "Success is not the absence of failure; it's the persistence through failure. - Aisha Tyler",
    "Opportunities are usually disguised as hard work, so most people don’t recognize them. - Ann Landers",
    "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
    "Do what you can with all you have, wherever you are. - Theodore Roosevelt",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Don’t wait for the perfect moment. Take the moment and make it perfect. - Unknown",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "The best revenge is massive success. - Frank Sinatra",
    "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "Success is the sum of small efforts, repeated day in and day out. - Robert Collier",
    "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. - Christian D. Larson",
    "Success is liking yourself, liking what you do, and liking how you do it. - Maya Angelou",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Don’t stop when you’re tired. Stop when you’re done. - Unknown",
    "It’s not whether you get knocked down, it’s whether you get up. - Vince Lombardi",
    "Don’t wait for opportunity. Create it. - Unknown",
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "The harder you work for something, the greater you’ll feel when you achieve it. - Unknown",
    "Nothing in the world can take the place of Persistence. Talent will not; nothing is more common than unsuccessful men with talent. - Calvin Coolidge",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "If you can dream it, you can do it. - Walt Disney",
    "Success is how high you bounce when you hit bottom. - George S. Patton",
    "Don’t let the noise of others’ opinions drown out your own inner voice. - Steve Jobs",
    "Success is not about how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Dream big and dare to fail. - Norman Vaughan",
    "Success is not how far you’ve gone, but how many people you’ve helped along the way. - Unknown",
    "You can’t cross the sea merely by standing and staring at the water. - Rabindranath Tagore",
    "Success is not measured by what you accomplish, but by the opposition you have encountered, and the courage with which you have maintained the struggle against overwhelming odds. - Orison Swett Marden",
    "You don’t have to be great to start, but you have to start to be great. - Zig Ziglar",
    "Success is the progressive realization of a worthy goal or ideal. - Earl Nightingale",
    "Success isn’t always about greatness. It’s about consistency. Consistent hard work leads to success. Greatness will come. - Dwayne Johnson",
    "Success is not in what you have, but who you are. - Bo Bennett",
    "The best way to predict your future is to create it. - Peter Drucker",
    "Failure is not the opposite of success; it’s part of success. - Arianna Huffington",
    "The road to success and the road to failure are almost exactly the same. - Colin R. Davis",
    "Do one thing every day that scares you. - Eleanor Roosevelt",
    "Success is not for the chosen few, but for those who choose it. - Unknown",
    "Success doesn’t come from what you do occasionally, it comes from what you do consistently. - Marie Forleo",
    "Success is achieved and maintained by those who try and keep trying. - W. Clement Stone"
]

billionaires = [
    {"name": "Jeff Bezos", "title": "Founder of Amazon", "net_worth": "$120B", "quote": "If you double the number of experiments you do per year, you’re going to double your inventiveness."},
    {"name": "Elon Musk", "title": "CEO of Tesla and SpaceX", "net_worth": "$200B", "quote": "When something is important enough, you do it even if the odds are not in your favor."},
    {"name": "Warren Buffett", "title": "Investor", "net_worth": "$118B", "quote": "Price is what you pay. Value is what you get."},
    {"name": "Bill Gates", "title": "Co-founder of Microsoft", "net_worth": "$115B", "quote": "Success is a lousy teacher. It seduces smart people into thinking they can't lose."},
    {"name": "Bernard Arnault", "title": "Chairman of LVMH", "net_worth": "$180B", "quote": "Luxury goods are the only area in which it is possible to make luxury margins."},
    {"name": "Mark Zuckerberg", "title": "Founder of Facebook", "net_worth": "$100B", "quote": "The biggest risk is not taking any risk."},
    {"name": "Larry Ellison", "title": "Co-founder of Oracle", "net_worth": "$108B", "quote": "When you innovate, you've got to be prepared for people telling you that you are nuts."},
    {"name": "Larry Page", "title": "Co-founder of Google", "net_worth": "$100B", "quote": "Always deliver more than expected."},
    {"name": "Sergey Brin", "title": "Co-founder of Google", "net_worth": "$96B", "quote": "Solving big problems is easier than solving little problems."},
    {"name": "Steve Jobs", "title": "Co-founder of Apple", "net_worth": "Legacy", "quote": "Innovation distinguishes between a leader and a follower."},
    {"name": "Oprah Winfrey", "title": "Media Mogul", "net_worth": "$2.5B", "quote": "The biggest adventure you can take is to live the life of your dreams."},
    {"name": "Richard Branson", "title": "Founder of Virgin Group", "net_worth": "$4B", "quote": "Business opportunities are like buses, there’s always another one coming."},
    {"name": "Amancio Ortega", "title": "Founder of Zara", "net_worth": "$70B", "quote": "The customer is the one who decides what fashion is."},
    {"name": "Carlos Slim Helu", "title": "Business Magnate", "net_worth": "$80B", "quote": "Maintain austerity in times of prosperity."},
    {"name": "Michael Bloomberg", "title": "Founder of Bloomberg LP", "net_worth": "$70B", "quote": "Don’t be afraid to assert yourself, have confidence in your abilities."},
    {"name": "Jack Ma", "title": "Founder of Alibaba", "net_worth": "$40B", "quote": "Never give up. Today is hard, tomorrow will be worse, but the day after tomorrow will be sunshine."},
    {"name": "Larry Fink", "title": "CEO of BlackRock", "net_worth": "$1B", "quote": "The biggest threat to our economy is inequality."},
    {"name": "Elon Musk", "title": "CEO of Tesla and SpaceX", "net_worth": "$200B", "quote": "Some people don't like change, but you need to embrace change if the alternative is disaster."},
    {"name": "Tim Cook", "title": "CEO of Apple", "net_worth": "$1.5B", "quote": "Let your joy be in your journey—not in some distant goal."},
    {"name": "Jeff Weiner", "title": "Executive Chairman of LinkedIn", "net_worth": "$2B", "quote": "Leadership is about making others better as a result of your presence and making sure that impact lasts in your absence."},
    {"name": "Indra Nooyi", "title": "Former CEO of PepsiCo", "net_worth": "$290M", "quote": "The glass ceiling will go away when women help other women break through it."},
    {"name": "Sundar Pichai", "title": "CEO of Alphabet (Google)", "net_worth": "$1.5B", "quote": "A lot of companies don't succeed over time. What do they fundamentally do wrong? They usually miss the future."},
    {"name": "Sheryl Sandberg", "title": "Former COO of Facebook", "net_worth": "$1.8B", "quote": "In the future, there will be no female leaders. There will just be leaders."},
    {"name": "Reed Hastings", "title": "Co-founder of Netflix", "net_worth": "$5B", "quote": "Do not tolerate brilliant jerks. The cost to teamwork is too high."},
    {"name": "Evan Spiegel", "title": "Co-founder of Snapchat", "net_worth": "$2B", "quote": "If you’re not doing something that you’re passionate about, you’re not going to put in the work."},
    {"name": "Richard Li", "title": "Chairman of PCCW", "net_worth": "$33B", "quote": "A good businessman makes others believe in him."},
    {"name": "Jeff Yass", "title": "Co-founder of 3G Capital", "net_worth": "$18B", "quote": "You don’t need to have everything figured out to take the first step."},
    {"name": "Stephen Schwarzman", "title": "CEO of Blackstone", "net_worth": "$21B", "quote": "You have to be able to deal with adversity and learn from it."},
    {"name": "Larry Ellison", "title": "Co-founder of Oracle", "net_worth": "$108B", "quote": "When you innovate, you've got to be prepared for people telling you that you are nuts."},
    {"name": "Mark Cuban", "title": "Owner of Dallas Mavericks", "net_worth": "$4.5B", "quote": "Work like there is someone working 24 hours a day to take it all away from you."},
    {"name": "Paul Allen", "title": "Co-founder of Microsoft", "net_worth": "Deceased", "quote": "The value of a company is a function of how good the company is at innovation."},
    {"name": "Michael Dell", "title": "Founder of Dell Technologies", "net_worth": "$38B", "quote": "You can never make the same mistake twice unless you fail to learn from it."},
    {"name": "John Malone", "title": "Chairman of Liberty Media", "net_worth": "$9.4B", "quote": "The key to success is being prepared to make mistakes."},
    {"name": "George Soros", "title": "Investor", "net_worth": "$8B", "quote": "I am only rich because I know when I’m wrong."},
    {"name": "Tom Steyer", "title": "Investor", "net_worth": "$1.6B", "quote": "If you have enough people who care, you can change the world."},
    {"name": "Eli Broad", "title": "Co-founder of KB Home", "net_worth": "$6.9B", "quote": "I don’t believe in retiring. I just believe in staying busy."},
    {"name": "Dustin Moskovitz", "title": "Co-founder of Facebook", "net_worth": "$20B", "quote": "The future will be about making big, long-term decisions."},
    {"name": "Brian Chesky", "title": "Co-founder of Airbnb", "net_worth": "$11.5B", "quote": "Don't be afraid to start small."},
    {"name": "Travis Kalanick", "title": "Co-founder of Uber", "net_worth": "$5.8B", "quote": "It’s always too early to quit."},
    {"name": "Jack Dorsey", "title": "Co-founder of Twitter", "net_worth": "$5B", "quote": "Make decisions quickly, adjust them slowly."},
    {"name": "Bobby Murphy", "title": "Co-founder of Snapchat", "net_worth": "$2B", "quote": "Focus on making the product something that people want."},
    {"name": "Evan Williams", "title": "Co-founder of Twitter", "net_worth": "$2B", "quote": "It’s better to have a small percentage of something big, than a big percentage of something small."},
    {"name": "Arianna Huffington", "title": "Founder of Huffington Post", "net_worth": "$100M", "quote": "Success is not about climbing the ladder; it’s about how you get there."},
    {"name": "Andrew Carnegie", "title": "Steel Magnate", "net_worth": "Deceased", "quote": "The man who dies rich dies disgraced."},
    {"name": "Thomas Edison", "title": "Inventor", "net_worth": "Deceased", "quote": "Genius is one percent inspiration, ninety-nine percent perspiration."},
    {"name": "Ralph Lauren", "title": "Fashion Designer", "net_worth": "$7B", "quote": "I don’t design clothes. I design dreams."},
    {"name": "Diane Hendricks", "title": "Chairman of ABC Supply", "net_worth": "$9B", "quote": "To succeed, you have to be passionate and persistent."},
    {"name": "Steve Ballmer", "title": "Former CEO of Microsoft", "net_worth": "$85B", "quote": "Greatness is a lot of small things done well."},
    {"name": "Phil Knight", "title": "Co-founder of Nike", "net_worth": "$44B", "quote": "The only time to be positive you’re in the right position is when you’re on the edge."},
    {"name": "Sara Blakely", "title": "Founder of Spanx", "net_worth": "$1.2B", "quote": "You can never be too busy to dream."},
    {"name": "Jack Ma", "title": "Founder of Alibaba", "net_worth": "$40B", "quote": "If you don't give up, you still have a chance."},
    {"name": "Catherine McKenna", "title": "Canadian Minister", "net_worth": "$1.5B", "quote": "Building strong economies requires investing in people."},
    {"name": "Alice Walton", "title": "Heir of Walmart", "net_worth": "$60B", "quote": "Philanthropy is the fuel for the engine of social change."},
    {"name": "Mukesh Ambani", "title": "Chairman of Reliance Industries", "net_worth": "$85B", "quote": "Anything and everything that can go digital is going digital."},
    {"name": "Francois Bettencourt Meyers", "title": "Heir of L'Oréal", "net_worth": "$90B", "quote": "Preserve the legacy while adapting to the future."},
    {"name": "Zhong Shanshan", "title": "Founder of Nongfu Spring", "net_worth": "$65B", "quote": "Focus on one thing and do it well."},
    {"name": "Gautam Adani", "title": "Chairman of Adani Group", "net_worth": "$75B", "quote": "Risk comes when you're not prepared."},
    {"name": "Shiv Nadar", "title": "Founder of HCL Technologies", "net_worth": "$30B", "quote": "The best way to predict the future is to create it."},
    {"name": "Li Ka-shing", "title": "Chairman of CK Hutchison Holdings", "net_worth": "$40B", "quote": "Vision is perhaps our greatest strength."},
    {"name": "Pony Ma", "title": "Founder of Tencent", "net_worth": "$50B", "quote": "Innovation stems from a culture of trust and curiosity."},
    {"name": "Ma Huateng", "title": "Chairman of Tencent", "net_worth": "$49B", "quote": "If you want to do great things, you must first dream big."},
    {"name": "Howard Schultz", "title": "CEO of Starbucks", "net_worth": "$4B", "quote": "Inspire and nurture the human spirit—one person, one cup, and one neighborhood at a time."},
    {"name": "Melinda French Gates", "title": "Co-chair of Gates Foundation", "net_worth": "$10B", "quote": "A woman with a voice is by definition a strong woman."},
    {"name": "Eric Yuan", "title": "Founder of Zoom", "net_worth": "$15B", "quote": "Empathy fuels innovation."},
    {"name": "Susanne Klatten", "title": "Heir of BMW", "net_worth": "$25B", "quote": "Sustainability is key to long-term success."},
    {"name": "Jim Simons", "title": "Founder of Renaissance Technologies", "net_worth": "$30B", "quote": "The data is your guide."},
    {"name": "Ken Griffin", "title": "Founder of Citadel", "net_worth": "$35B", "quote": "Decisions driven by data are often the best."},
    {"name": "Akio Toyoda", "title": "President of Toyota", "net_worth": "$1B", "quote": "There’s no growth without change."},
    {"name": "Barbara Corcoran", "title": "Real Estate Mogul", "net_worth": "$100M", "quote": "Don’t you dare underestimate the power of your instinct."},
    {"name": "David Tepper", "title": "Founder of Appaloosa Management", "net_worth": "$20B", "quote": "There's always money to be made in the markets."},
    {"name": "Masayoshi Son", "title": "Founder of SoftBank", "net_worth": "$23B", "quote": "Vision is the art of seeing the invisible."},
    {"name": "Daniel Ek", "title": "Founder of Spotify", "net_worth": "$5B", "quote": "People should be able to hear the music they love anywhere."},
    {"name": "Hans Vestberg", "title": "CEO of Verizon", "net_worth": "$100M", "quote": "Connectivity is a fundamental right for all."},
    {"name": "Marc Benioff", "title": "CEO of Salesforce", "net_worth": "$8B", "quote": "The business of business is improving the state of the world."},
    {"name": "Peter Thiel", "title": "Co-founder of PayPal", "net_worth": "$6B", "quote": "Brilliant thinking is rare, but courage is in shorter supply."},
    {"name": "Drew Houston", "title": "Founder of Dropbox", "net_worth": "$3B", "quote": "Don’t worry about failure; you only have to be right once."},
    {"name": "Stewart Butterfield", "title": "Co-founder of Slack", "net_worth": "$1B", "quote": "The best products are built from personal frustration."},
    {"name": "Robert Smith", "title": "Founder of Vista Equity Partners", "net_worth": "$10B", "quote": "Success is only as meaningful as the impact it creates."},
    {"name": "Serena Williams", "title": "Tennis Star and Investor", "net_worth": "$300M", "quote": "Every champion was once a contender who didn’t give up."},
    {"name": "Narayana Murthy", "title": "Founder of Infosys", "net_worth": "$4B", "quote": "Growth is painful. Change is painful. But nothing is as painful as staying stuck somewhere you don't belong."},
    {"name": "Mike Cannon-Brookes", "title": "Co-founder of Atlassian", "net_worth": "$15B", "quote": "Think big, start small, scale fast."},
    {"name": "Jim Pattison", "title": "Chairman of The Jim Pattison Group", "net_worth": "$12B", "quote": "Make your decisions based on long-term value."},
    {"name": "Vinod Khosla", "title": "Founder of Khosla Ventures", "net_worth": "$5B", "quote": "Failure often teaches more than success ever could."},
    {"name": "Eric Schmidt", "title": "Former CEO of Google", "net_worth": "$20B", "quote": "Find the leverage point and apply maximum pressure."},
    {"name": "Ratan Tata", "title": "Chairman Emeritus of Tata Group", "net_worth": "$1B", "quote": "Take the stones people throw at you, and use them to build a monument."},
    {"name": "Oprah Winfrey", "title": "Media Mogul", "net_worth": "$2.8B", "quote": "Turn your wounds into wisdom."},
    {"name": "Mark Cuban", "title": "Entrepreneur and Investor", "net_worth": "$5B", "quote": "Wherever I see people doing something the way it’s always been done, the way it’s ‘supposed’ to be done, that’s just a big red flag to me."},
    {"name": "Carlos Ghosn", "title": "Former CEO of Renault-Nissan", "net_worth": "$120M", "quote": "Success depends on how much you learn from failure."}
]

@router.message(Command(commands=["eliteagent"]))
async def send_welcome(message: Message):
    """Handle /start and /help commands."""
    await message.reply("Chat with me /aiagent <your text> or type /elite to get inspired by the wealthiest and most successful people in the world! ")


@router.message(Command(commands=["elite"]))
async def elite_command(message: Message):
    """Handle the /elite command (without any input) to send quotes, facts, or billionaire insights."""
    # Choose the type of response (fact, quote, billionaire)
    response_type = random.choice(["fact", "quote", "billionaire"])

    if response_type == "fact":
        fact = random.choice(facts)
        await message.reply(fact)
    
    elif response_type == "quote":
        quote = random.choice(quotes)
        await message.reply(quote)
    
    elif response_type == "billionaire":
        billionaire = random.choice(billionaires)
        billionaire_info = (f"{billionaire['name']}, {billionaire['title']} | Net Worth: {billionaire['net_worth']}\n"
                            f"Quote: {billionaire['quote']}")
        await message.reply(billionaire_info)


@router.message(Command(commands=["aiagent"]))
async def chat_with_gpt(message: Message):
    """Handle the /aiagent <text> command to chat with ChatGPT."""
    # Remove the "/aiagent" command and get the user's message
    user_message = message.text[9:].strip()  # Remove "/aiagent " from the message

    if user_message:
        try:
            # Send the user's message to OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a motivational bot to show people how wealthy they can be, how they can become elite and how to be top 1% in the world. Please make short but catchy answers and without hashtags. Try to act like Tony Montana."},
                    {"role": "user", "content": user_message},
                ]
            )
            # Extract the response text
            gpt_response = response["choices"][0]["message"]["content"]

            # Send the response back to the user
            await message.reply(gpt_response)
        except Exception as e:
            logging.error(f"Error: {e}")
            await message.reply("Sorry, something went wrong. Please try again later.")


@router.chat_member()
async def on_user_joined(member_update: ChatMemberUpdated):
    """Handle when a new member joins the group."""
    if member_update.new_chat_member.status == "member":
        new_member = member_update.new_chat_member.user
        welcome_message = (
            f"Welcome to the future top 1% in the world, {new_member.first_name}! 🎉\n"
            "Chat with me /aiagent <your text> or type /elite to get inspired by the wealthiest and most successful people in the world! Use /eliteagent for help."
        )
        await bot.send_message(member_update.chat.id, welcome_message)


async def main():
    # Register the router with the dispatcher
    dp.include_router(router)

    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())