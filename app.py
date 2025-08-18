from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', generate_password_hash('default-secret-key'))

# Configurazione
app.config.update(
    SESSION_PERMANENT=False,
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minuti
    TEMPLATES_AUTO_RELOAD=True
)

# Database delle domande
questions = [
# Section 1: History of the United States (30 Questions)
    {
        "id": 1,
        "question": "What is the supreme law of the land?",
        "options": [
            "The Declaration of Independence",
            "The Articles of Confederation",
            "The Bill of Rights",
            "The Constitution"
        ],
        "answer": "The Constitution",
        "explanation": "The Constitution is the supreme law of the United States."
    },
    {
        "id": 2,
        "question": "Who wrote the Declaration of Independence?",
        "options": [
            "Benjamin Franklin",
            "Thomas Jefferson",
            "John Adams",
            "George Washington"
        ],
        "answer": "Thomas Jefferson",
        "explanation": "Thomas Jefferson was the primary author of the Declaration of Independence."
    },
    {
        "id": 3,
        "question": "What year was the Constitution written?",
        "options": ["1776", "1787", "1801", "1791"],
        "answer": "1787",
        "explanation": "The Constitution was drafted in 1787 during the Constitutional Convention."
    },
    {
        "id": 4,
        "question": "What is one reason colonists came to America?",
        "options": [
            "To escape taxation",
            "For religious freedom",
            "To fight the British",
            "To own slaves"
        ],
        "answer": "For religious freedom",
        "explanation": "Many colonists came to America seeking freedom to practice their religion."
    },
    {
        "id": 5,
        "question": "Who was the first President of the United States?",
        "options": [
            "Abraham Lincoln",
            "Thomas Jefferson",
            "George Washington",
            "John Adams"
        ],
        "answer": "George Washington",
        "explanation": "George Washington was unanimously elected as the first President in 1789."
    },
    {
        "id": 6,
        "question": "When was the Declaration of Independence adopted?",
        "options": [
            "July 4, 1776",
            "July 4, 1781",
            "December 25, 1776",
            "January 1, 1776"
        ],
        "answer": "July 4, 1776",
        "explanation": "The Declaration was adopted on July 4, now celebrated as Independence Day."
    },
    {
        "id": 7,
        "question": "What did the Declaration of Independence do?",
        "options": [
            "Declared independence from France",
            "Declared independence from Great Britain",
            "Established the Constitution",
            "Created the Bill of Rights"
        ],
        "answer": "Declared independence from Great Britain",
        "explanation": "It announced the colonies' separation from British rule."
    },
    {
        "id": 8,
        "question": "What are two rights in the Declaration of Independence?",
        "options": [
            "Life and liberty",
            "Freedom of religion and speech",
            "Trial by jury and voting rights",
            "Equality and the right to bear arms"
        ],
        "answer": "Life and liberty",
        "explanation": "The Declaration states people have rights to life, liberty, and pursuit of happiness."
    },
    {
        "id": 9,
        "question": "What group of people was taken to America and sold as slaves?",
        "options": [
            "Native Americans",
            "Europeans",
            "Africans",
            "Asians"
        ],
        "answer": "Africans",
        "explanation": "Millions of Africans were forcibly brought to America through the slave trade."
    },
    {
        "id": 10,
        "question": "Who is called the \"Father of Our Country\"?",
        "options": [
            "John Adams",
            "George Washington",
            "James Madison",
            "Thomas Jefferson"
        ],
        "answer": "George Washington",
        "explanation": "Washington is called the \"Father of Our Country\" for his leadership."
    },
    {
        "id": 11,
        "question": "What was one important thing that Abraham Lincoln did?",
        "options": [
            "Signed the Constitution",
            "Issued the Emancipation Proclamation",
            "Declared independence from Great Britain",
            "Drafted the Bill of Rights"
        ],
        "answer": "Issued the Emancipation Proclamation",
        "explanation": "Lincoln issued the Proclamation freeing enslaved people in Confederate states."
    },
    {
        "id": 12,
        "question": "What movement tried to end racial discrimination?",
        "options": [
            "The Civil Rights Movement",
            "The Abolitionist Movement",
            "The Women's Suffrage Movement",
            "The Temperance Movement"
        ],
        "answer": "The Civil Rights Movement",
        "explanation": "This movement sought to end racial discrimination and secure equal rights."
    },
    {
        "id": 13,
        "question": "Who was Martin Luther King Jr.?",
        "options": [
            "A U.S. President",
            "A civil rights leader",
            "A Supreme Court Justice",
            "An author of the Constitution"
        ],
        "answer": "A civil rights leader",
        "explanation": "MLK Jr. was a key leader in the Civil Rights Movement."
    },
    {
        "id": 14,
        "question": "What territory did the United States buy from France in 1803?",
        "options": ["Texas", "Alaska", "Louisiana", "Oregon"],
        "answer": "Louisiana",
        "explanation": "The Louisiana Purchase doubled the size of the United States."
    },
    {
        "id": 15,
        "question": "What war was fought by the United States in the 1800s?",
        "options": [
            "World War I",
            "The Civil War",
            "The Korean War",
            "The Gulf War"
        ],
        "answer": "The Civil War",
        "explanation": "The Civil War was fought from 1861 to 1865 over slavery and states' rights."
    },
    {
        "id": 16,
        "question": "What was the primary issue leading to the Civil War?",
        "options": [
            "Taxation without representation",
            "Slavery",
            "Trade disputes with Great Britain",
            "The Louisiana Purchase"
        ],
        "answer": "Slavery",
        "explanation": "Slavery was a major cause dividing Northern and Southern states."
    },
    {
        "id": 17,
        "question": "What is one thing Benjamin Franklin is famous for?",
        "options": [
            "Being the first President",
            "Writing the Declaration of Independence",
            "Serving as a U.S. diplomat",
            "Leading the Civil War"
        ],
        "answer": "Serving as a U.S. diplomat",
        "explanation": "Franklin was instrumental in securing French support during the Revolution."
    },
    {
        "id": 18,
        "question": "Who was Susan B. Anthony?",
        "options": [
            "A women's rights activist",
            "A U.S. President",
            "A Civil War general",
            "A signer of the Declaration of Independence"
        ],
        "answer": "A women's rights activist",
        "explanation": "Anthony was a key figure in the women's suffrage movement."
    },
    {
        "id": 19,
        "question": "What major event happened on September 11, 2001?",
        "options": [
            "Hurricane Katrina struck",
            "Terrorist attacks on the U.S.",
            "The stock market crash",
            "The end of the Cold War"
        ],
        "answer": "Terrorist attacks on the U.S.",
        "explanation": "Al-Qaeda terrorists attacked the World Trade Center and Pentagon."
    },
    {
        "id": 20,
        "question": "What is one reason the United States entered World War II?",
        "options": [
            "To support the Axis powers",
            "The bombing of Pearl Harbor",
            "To spread communism",
            "The Treaty of Versailles"
        ],
        "answer": "The bombing of Pearl Harbor",
        "explanation": "Japan's attack on Pearl Harbor prompted U.S. entry into WWII."
    },
    {
        "id": 21,
        "question": "Who was President during the Great Depression and World War II?",
        "options": [
            "Woodrow Wilson",
            "Harry Truman",
            "Franklin D. Roosevelt",
            "Dwight D. Eisenhower"
        ],
        "answer": "Franklin D. Roosevelt",
        "explanation": "FDR led the nation during the Great Depression and most of WWII."
    },
    {
        "id": 22,
        "question": "Who did the United States fight in World War II?",
        "options": [
            "Germany, Italy, and Japan",
            "Russia, Germany, and Italy",
            "China, Japan, and Vietnam",
            "France, Germany, and Spain"
        ],
        "answer": "Germany, Italy, and Japan",
        "explanation": "These nations formed the Axis Powers opposed by the U.S. in WWII."
    },
    {
        "id": 23,
        "question": "Who was President during World War I?",
        "options": [
            "Franklin Roosevelt",
            "Woodrow Wilson",
            "Theodore Roosevelt",
            "Herbert Hoover"
        ],
        "answer": "Woodrow Wilson",
        "explanation": "Wilson was President during WWI and helped found the League of Nations."
    },
    {
        "id": 24,
        "question": "When was the Constitution written?",
        "options": ["1776", "1787", "1801", "1791"],
        "answer": "1787",
        "explanation": "The Constitution was written in 1787 to establish the U.S. government framework."
    },
    {
        "id": 25,
        "question": "What are the first three words of the Constitution?",
        "options": [
            "\"We the People\"",
            "\"Four score and seven\"",
            "\"In God We Trust\"",
            "\"Life, liberty, happiness\""
        ],
        "answer": "\"We the People\"",
        "explanation": "These words signify government power comes from citizens."
    },
    {
        "id": 26,
        "question": "What is freedom of religion?",
        "options": [
            "The ability to practice or not practice any religion",
            "Mandatory attendance at church",
            "Freedom from paying taxes to religious organizations",
            "Voting rights based on religion"
        ],
        "answer": "The ability to practice or not practice any religion",
        "explanation": "Freedom of religion is guaranteed by the First Amendment."
    },
    {
        "id": 27,
        "question": "Who makes federal laws?",
        "options": [
            "Congress",
            "The President",
            "The Supreme Court",
            "State legislatures"
        ],
        "answer": "Congress",
        "explanation": "Congress, composed of Senate and House, creates federal laws."
    },
    {
        "id": 28,
        "question": "What is the Bill of Rights?",
        "options": [
            "The first 10 amendments to the Constitution",
            "A list of laws passed by Congress",
            "The Declaration of Independence",
            "A treaty with Britain"
        ],
        "answer": "The first 10 amendments to the Constitution",
        "explanation": "The Bill of Rights guarantees fundamental freedoms."
    },
    {
        "id": 29,
        "question": "Who wrote the Federalist Papers?",
        "options": [
            "Alexander Hamilton, James Madison, and John Jay",
            "George Washington and Thomas Jefferson",
            "Benjamin Franklin and John Adams",
            "Samuel Adams and Paul Revere"
        ],
        "answer": "Alexander Hamilton, James Madison, and John Jay",
        "explanation": "They wrote the Papers to support Constitution ratification."
    },
    {
        "id": 30,
        "question": "What is one right guaranteed in the First Amendment?",
        "options": [
            "Freedom of speech",
            "The right to bear arms",
            "The right to a fair trial",
            "The right to vote"
        ],
        "answer": "Freedom of speech",
        "explanation": "The First Amendment protects freedom of speech, religion, press, and assembly."
    },
    # Section 2: U.S. Government Structure (40 Questions)
    {
        "id": 31,
        "question": "What are the three branches of the government?",
        "options": [
            "Executive, Legislative, and Judicial",
            "State, Federal, and Local",
            "Congress, Supreme Court, and Military",
            "President, Vice President, and Cabinet"
        ],
        "answer": "Executive, Legislative, and Judicial",
        "explanation": "These three branches form the U.S. government system with checks and balances."
    },
    {
        "id": 32,
        "question": "Who makes federal laws?",
        "options": [
            "The President",
            "The Supreme Court",
            "Congress",
            "State Legislatures"
        ],
        "answer": "Congress",
        "explanation": "Congress is responsible for creating federal laws."
    },
    {
        "id": 33,
        "question": "How many U.S. Senators are there?",
        "options": ["50", "100", "435", "200"],
        "answer": "100",
        "explanation": "Each state elects two Senators for a total of 100."
    },
    {
        "id": 34,
        "question": "How many voting members are in the House of Representatives?",
        "options": ["50", "100", "435", "535"],
        "answer": "435",
        "explanation": "The number of Representatives is based on state population."
    },
    {
        "id": 35,
        "question": "We elect a U.S. Senator for how many years?",
        "options": ["2 years", "4 years", "6 years", "8 years"],
        "answer": "6 years",
        "explanation": "U.S. Senators serve six-year terms."
    },
    {
        "id": 36,
        "question": "We elect a U.S. Representative for how many years?",
        "options": ["2 years", "4 years", "6 years", "8 years"],
        "answer": "2 years",
        "explanation": "Representatives serve two-year terms."
    },
    {
        "id": 37,
        "question": "Who does a U.S. Senator represent?",
        "options": [
            "All people of the state",
            "Only registered voters in the state",
            "Only the state legislature",
            "Citizens living abroad"
        ],
        "answer": "All people of the state",
        "explanation": "Senators represent all residents of their states."
    },
    {
        "id": 38,
        "question": "Why do some states have more Representatives than others?",
        "options": [
            "Because of the state's population",
            "Because the state has more land",
            "Because the state has a higher income level",
            "Because the state has more senators"
        ],
        "answer": "Because of the state's population",
        "explanation": "States with larger populations have more Representatives."
    },
    {
        "id": 39,
        "question": "What is the name of the President of the United States now?",
        "options": [
            "Joe Biden",
            "Kamala Harris",
            "Donald Trump",
            "Mike Pence"
        ],
        "answer": "Joe Biden",
        "explanation": "Current as of 2023 - update as needed for accuracy."
    },
    {
        "id": 40,
        "question": "What is the name of the Vice President of the United States now?",
        "options": [
            "Joe Biden",
            "Kamala Harris",
            "Mike Pence",
            "Nancy Pelosi"
        ],
        "answer": "Kamala Harris",
        "explanation": "Current as of 2023 - update as needed for accuracy."
    },
    {
        "id": 41,
        "question": "If the President can no longer serve, who becomes President?",
        "options": [
            "The Vice President",
            "The Speaker of the House",
            "The Secretary of State",
            "The Chief Justice"
        ],
        "answer": "The Vice President",
        "explanation": "The Vice President is first in the presidential line of succession."
    },
    {
        "id": 42,
        "question": "If both the President and the Vice President can no longer serve, who becomes President?",
        "options": [
            "The Speaker of the House",
            "The Chief Justice",
            "The Secretary of State",
            "The Majority Leader of the Senate"
        ],
        "answer": "The Speaker of the House",
        "explanation": "The Speaker is next in line after the Vice President."
    },
    {
        "id": 43,
        "question": "Who is the Commander in Chief of the military?",
        "options": [
            "The Secretary of Defense",
            "The President",
            "The Speaker of the House",
            "The Vice President"
        ],
        "answer": "The President",
        "explanation": "The President oversees the U.S. armed forces as Commander in Chief."
    },
    {
        "id": 44,
        "question": "Who signs bills to become laws?",
        "options": [
            "The President",
            "The Vice President",
            "The Speaker of the House",
            "The Chief Justice"
        ],
        "answer": "The President",
        "explanation": "Bills passed by Congress must be signed by the President to become law."
    },
    {
        "id": 45,
        "question": "Who vetoes bills?",
        "options": [
            "The President",
            "The Vice President",
            "The Speaker of the House",
            "The Chief Justice"
        ],
        "answer": "The President",
        "explanation": "The President has power to veto bills passed by Congress."
    },
    {
        "id": 46,
        "question": "What does the President's Cabinet do?",
        "options": [
            "Makes laws",
            "Advises the President",
            "Commands the military",
            "Approves treaties"
        ],
        "answer": "Advises the President",
        "explanation": "The Cabinet consists of department heads who advise the President."
    },
    {
        "id": 47,
        "question": "What are two Cabinet-level positions?",
        "options": [
            "Secretary of State and Secretary of Defense",
            "Chief Justice and Speaker of the House",
            "Attorney General and Senate Majority Leader",
            "Secretary of Commerce and Chief of Staff"
        ],
        "answer": "Secretary of State and Secretary of Defense",
        "explanation": "These are examples of Cabinet-level positions."
    },
    {
        "id": 48,
        "question": "What does the Judicial Branch do?",
        "options": [
            "Reviews laws and resolves disputes",
            "Creates laws",
            "Commands the military",
            "Approves treaties"
        ],
        "answer": "Reviews laws and resolves disputes",
        "explanation": "The Judicial Branch interprets laws and ensures they comply with the Constitution."
    },
    {
        "id": 49,
        "question": "What is the highest court in the United States?",
        "options": [
            "The Supreme Court",
            "The Federal Court of Appeals",
            "The Constitutional Court",
            "The District Court"
        ],
        "answer": "The Supreme Court",
        "explanation": "The Supreme Court is the highest court with ultimate authority."
    },
    {
        "id": 50,
        "question": "How many justices are on the Supreme Court?",
        "options": ["7", "9", "11", "13"],
        "answer": "9",
        "explanation": "The Supreme Court traditionally has nine justices."
    },
    {
        "id": 51,
        "question": "Who is the Chief Justice of the United States now?",
        "options": [
            "John Roberts",
            "Clarence Thomas",
            "Sonia Sotomayor",
            "Neil Gorsuch"
        ],
        "answer": "John Roberts",
        "explanation": "John Roberts is the current Chief Justice (as of 2023)."
    },
    {
        "id": 52,
        "question": "Under our Constitution, some powers belong to the federal government. What is one power of the federal government?",
        "options": [
            "To print money",
            "To set up schools",
            "To issue driver's licenses",
            "To regulate zoning laws"
        ],
        "answer": "To print money",
        "explanation": "Printing money is a power reserved for the federal government."
    },
    {
        "id": 53,
        "question": "Under our Constitution, some powers belong to the states. What is one power of the states?",
        "options": [
            "Provide schooling and education",
            "Print money",
            "Declare war",
            "Create an army"
        ],
        "answer": "Provide schooling and education",
        "explanation": "Education is primarily a state responsibility."
    },
    {
        "id": 54,
        "question": "Who is the Governor of your state now?",
        "options": [
            "Answers vary",
            "Joe Biden",
            "Kamala Harris",
            "Nancy Pelosi"
        ],
        "answer": "Answers vary",
        "explanation": "The Governor is the head of the state's executive branch."
    },
    {
        "id": 55,
        "question": "What is the capital of your state?",
        "options": [
            "Answers vary",
            "Washington, D.C.",
            "New York City",
            "Chicago"
        ],
        "answer": "Answers vary",
        "explanation": "Each state has its own capital city."
    },
    {
        "id": 56,
        "question": "What are the two major political parties in the United States?",
        "options": [
            "Democratic and Republican",
            "Labor and Green",
            "Independent and Libertarian",
            "Federalist and Whig"
        ],
        "answer": "Democratic and Republican",
        "explanation": "These are the two major political parties."
    },
    {
        "id": 57,
        "question": "What is the political party of the President now?",
        "options": [
            "Democratic Party",
            "Republican Party",
            "Green Party",
            "Libertarian Party"
        ],
        "answer": "Democratic Party",
        "explanation": "Current as of 2023 - update as needed for accuracy."
    },
    {
        "id": 58,
        "question": "What is the name of the Speaker of the House of Representatives now?",
        "options": [
            "Answers vary",
            "Nancy Pelosi",
            "Kevin McCarthy",
            "Chuck Schumer"
        ],
        "answer": "Answers vary",
        "explanation": "The Speaker's name depends on the current officeholder."
    },
    {
        "id": 59,
        "question": "How old do citizens have to be to vote for President?",
        "options": ["16", "18", "21", "25"],
        "answer": "18",
        "explanation": "The voting age was lowered to 18 by the 26th Amendment."
    },
    {
        "id": 60,
        "question": "When is the last day you can send in federal income tax forms?",
        "options": ["April 15", "May 1", "June 30", "December 31"],
        "answer": "April 15",
        "explanation": "Federal income taxes are typically due on April 15 each year."
    },
    {
        "id": 61,
        "question": "When must all men register for the Selective Service?",
        "options": ["At age 18", "At age 21", "Before age 16", "At age 25"],
        "answer": "At age 18",
        "explanation": "Men aged 18-25 must register for potential military draft."
    },
    {
        "id": 62,
        "question": "What is the rule of law?",
        "options": [
            "Everyone must follow the law",
            "Only government officials must follow the law",
            "Laws apply only to citizens",
            "Laws can be ignored if inconvenient"
        ],
        "answer": "Everyone must follow the law",
        "explanation": "The rule of law means no one is above the law."
    },
    {
        "id": 63,
        "question": "What is one responsibility that is only for United States citizens?",
        "options": [
            "Serve on a jury",
            "Pay taxes",
            "Obey traffic laws",
            "Vote in local elections"
        ],
        "answer": "Serve on a jury",
        "explanation": "Jury service is a responsibility unique to U.S. citizens."
    },
    {
        "id": 64,
        "question": "What are two ways that Americans can participate in their democracy?",
        "options": [
            "Voting and running for office",
            "Paying taxes and serving on a jury",
            "Working and joining the military",
            "Obeying laws and driving legally"
        ],
        "answer": "Voting and running for office",
        "explanation": "These are key ways to participate in democracy."
    },
    {
        "id": 65,
        "question": "Who is in charge of the Executive Branch?",
        "options": [
            "The President",
            "The Vice President",
            "The Speaker of the House",
            "The Chief Justice"
        ],
        "answer": "The President",
        "explanation": "The President leads the Executive Branch."
    },
    {
        "id": 66,
        "question": "What does the Constitution do?",
        "options": [
            "Sets up the government",
            "Declares war",
            "Elects the President",
            "Determines state laws"
        ],
        "answer": "Sets up the government",
        "explanation": "The Constitution outlines the federal government structure."
    },
    {
        "id": 67,
        "question": "What are the two parts of the U.S. Congress?",
        "options": [
            "Senate and Supreme Court",
            "House of Representatives and Executive Branch",
            "Senate and House of Representatives",
            "President and Vice President"
        ],
        "answer": "Senate and House of Representatives",
        "explanation": "Congress is divided into these two chambers."
    },
    {
        "id": 68,
        "question": "Who can veto bills?",
        "options": [
            "The President",
            "The Supreme Court",
            "The Vice President",
            "The Speaker of the House"
        ],
        "answer": "The President",
        "explanation": "The President has authority to veto bills."
    },
    {
        "id": 69,
        "question": "Who advises the President?",
        "options": [
            "The Cabinet",
            "Congress",
            "The Supreme Court",
            "State Governors"
        ],
        "answer": "The Cabinet",
        "explanation": "The Cabinet advises the President on key issues."
    },
    {
        "id": 70,
        "question": "What is one power of the states under the Constitution?",
        "options": [
            "Provide schooling and education",
            "Declare war",
            "Print money",
            "Create treaties"
        ],
        "answer": "Provide schooling and education",
        "explanation": "Education is primarily a state responsibility."
    },
    # Section 3: Geography of the United States (20 Questions)
    {
        "id": 71,
        "question": "What ocean is on the East Coast of the United States?",
        "options": [
            "The Pacific Ocean",
            "The Atlantic Ocean",
            "The Indian Ocean",
            "The Arctic Ocean"
        ],
        "answer": "The Atlantic Ocean",
        "explanation": "The Atlantic Ocean borders the East Coast."
    },
    {
        "id": 72,
        "question": "What ocean is on the West Coast of the United States?",
        "options": [
            "The Atlantic Ocean",
            "The Pacific Ocean",
            "The Arctic Ocean",
            "The Indian Ocean"
        ],
        "answer": "The Pacific Ocean",
        "explanation": "The Pacific Ocean borders the West Coast."
    },
    {
        "id": 73,
        "question": "Name one of the two longest rivers in the United States.",
        "options": [
            "Mississippi River",
            "Hudson River",
            "Colorado River",
            "Delaware River"
        ],
        "answer": "Mississippi River",
        "explanation": "The Mississippi is one of the two longest rivers (with the Missouri)."
    },
    {
        "id": 74,
        "question": "What is the capital of the United States?",
        "options": [
            "New York",
            "Boston",
            "Washington, D.C.",
            "Philadelphia"
        ],
        "answer": "Washington, D.C.",
        "explanation": "Washington, D.C. is the U.S. capital."
    },
    {
        "id": 75,
        "question": "Name one state that borders Canada.",
        "options": ["Texas", "Michigan", "Alabama", "Florida"],
        "answer": "Michigan",
        "explanation": "Michigan is one of 13 states bordering Canada."
    },
    {
        "id": 76,
        "question": "Name one state that borders Mexico.",
        "options": ["Nevada", "Texas", "Tennessee", "Colorado"],
        "answer": "Texas",
        "explanation": "Texas is one of four states bordering Mexico."
    },
    {
        "id": 77,
        "question": "What is the capital of your state?",
        "options": [
            "Answers vary",
            "Washington, D.C.",
            "Sacramento",
            "Atlanta"
        ],
        "answer": "Answers vary",
        "explanation": "Each state has its own capital city."
    },
    {
        "id": 78,
        "question": "Name a U.S. territory.",
        "options": ["Puerto Rico", "Canada", "Hawaii", "Alaska"],
        "answer": "Puerto Rico",
        "explanation": "Puerto Rico is a U.S. territory."
    },
    {
        "id": 79,
        "question": "What is the name of the national anthem?",
        "options": [
            "\"America the Beautiful\"",
            "\"The Star-Spangled Banner\"",
            "\"God Bless America\"",
            "\"My Country, 'Tis of Thee\""
        ],
        "answer": "\"The Star-Spangled Banner\"",
        "explanation": "This is the U.S. national anthem."
    },
    {
        "id": 80,
        "question": "Why does the flag have 13 stripes?",
        "options": [
            "Because there were 13 colonies",
            "Because there are 13 amendments",
            "Because there are 13 states",
            "Because it symbolizes 13 presidents"
        ],
        "answer": "Because there were 13 colonies",
        "explanation": "The stripes represent the original 13 colonies."
    },
    {
        "id": 81,
        "question": "Why does the flag have 50 stars?",
        "options": [
            "Because there are 50 presidents",
            "Because there are 50 states",
            "Because there are 50 territories",
            "Because there are 50 amendments"
        ],
        "answer": "Because there are 50 states",
        "explanation": "Each star represents a state in the Union."
    },
    {
        "id": 82,
        "question": "What is the tallest mountain in the United States?",
        "options": [
            "Mount McKinley (Denali)",
            "Mount Everest",
            "Mount Whitney",
            "Mount Rainier"
        ],
        "answer": "Mount McKinley (Denali)",
        "explanation": "Denali in Alaska is the tallest U.S. mountain."
    },
    {
        "id": 83,
        "question": "What is the largest state by area in the United States?",
        "options": ["Texas", "California", "Alaska", "Montana"],
        "answer": "Alaska",
        "explanation": "Alaska is the largest state by area."
    },
    {
        "id": 84,
        "question": "What is the smallest state by area in the United States?",
        "options": [
            "Rhode Island",
            "Delaware",
            "Vermont",
            "Connecticut"
        ],
        "answer": "Rhode Island",
        "explanation": "Rhode Island is the smallest state by area."
    },
    {
        "id": 85,
        "question": "Which U.S. state is an island chain?",
        "options": ["Alaska", "Hawaii", "Florida", "California"],
        "answer": "Hawaii",
        "explanation": "Hawaii is an island chain in the Pacific."
    },
    {
        "id": 86,
        "question": "Which state is known as the \"Land of 10,000 Lakes\"?",
        "options": ["Wisconsin", "Minnesota", "Michigan", "New York"],
        "answer": "Minnesota",
        "explanation": "Minnesota has numerous lakes."
    },
    {
        "id": 87,
        "question": "What is the name of the desert in the southwestern United States?",
        "options": [
            "The Mojave Desert",
            "The Sahara Desert",
            "The Gobi Desert",
            "The Great Basin Desert"
        ],
        "answer": "The Mojave Desert",
        "explanation": "The Mojave is in the southwestern U.S."
    },
    {
        "id": 88,
        "question": "What U.S. state has the most national parks?",
        "options": ["Alaska", "California", "Utah", "Colorado"],
        "answer": "California",
        "explanation": "California has the most national parks."
    },
    {
        "id": 89,
        "question": "What is the largest river by volume in the United States?",
        "options": [
            "Mississippi River",
            "Missouri River",
            "Colorado River",
            "Yukon River"
        ],
        "answer": "Mississippi River",
        "explanation": "The Mississippi has the greatest water volume."
    },
    {
        "id": 90,
        "question": "Which U.S. state is nicknamed \"The Sunshine State\"?",
        "options": ["California", "Florida", "Arizona", "Nevada"],
        "answer": "Florida",
        "explanation": "Florida is known for its sunny weather."
    },
    # Section 4: Rights and Responsibilities of U.S. Citizens (10 Questions)
    {
        "id": 91,
        "question": "What is one responsibility that is only for United States citizens?",
        "options": [
            "Serve on a jury",
            "Pay taxes",
            "Obey traffic laws",
            "Join the military"
        ],
        "answer": "Serve on a jury",
        "explanation": "Jury service is a citizen responsibility."
    },
    {
        "id": 92,
        "question": "Name one right only for United States citizens.",
        "options": [
            "The right to vote in federal elections",
            "Freedom of speech",
            "Freedom of religion",
            "The right to bear arms"
        ],
        "answer": "The right to vote in federal elections",
        "explanation": "Only citizens can vote in federal elections."
    },
    {
        "id": 93,
        "question": "What are two rights of everyone living in the United States?",
        "options": [
            "Freedom of speech and freedom of religion",
            "The right to vote and the right to bear arms",
            "Freedom of speech and the right to a fair trial",
            "The right to bear arms and the right to work"
        ],
        "answer": "Freedom of speech and freedom of religion",
        "explanation": "These are fundamental rights for all in the U.S."
    },
    {
    "id": 94,
    "question": "What do we show loyalty to when we say the Pledge of Allegiance?",
    "options": [
        "The President",
        "The United States and the flag",
        "Congress",
        "The military"
    ],
    "answer": "The United States and the flag",
    "explanation": "The Pledge of Allegiance is a vow of loyalty to the country and its values."
},
{
    "id": 95,
    "question": "What is one promise you make when you become a United States citizen?",
    "options": [
        "To obey the laws of the United States",
        "To always vote in elections",
        "To pay taxes on time",
        "To serve in the military"
    ],
    "answer": "To obey the laws of the United States",
    "explanation": "New citizens promise to uphold and respect U.S. laws as part of their oath of allegiance."
},
{
    "id": 96,
    "question": "How old do citizens have to be to vote for President?",
    "options": [
        "16",
        "18",
        "21",
        "25"
    ],
    "answer": "18",
    "explanation": "Citizens must be at least 18 years old to vote in federal elections."
},
{
    "id": 97,
    "question": "What are two ways that Americans can participate in their democracy?",
    "options": [
        "Voting and running for office",
        "Paying taxes and serving on a jury",
        "Joining the military and working",
        "Obeying the law and driving legally"
    ],
    "answer": "Voting and running for office",
    "explanation": "Participating in elections and serving in public office are two key ways Americans engage in democracy."
},
{
    "id": 98,
    "question": "When is the last day you can send in federal income tax forms?",
    "options": [
        "April 1",
        "April 15",
        "May 15",
        "December 31"
    ],
    "answer": "April 15",
    "explanation": "Federal income tax returns are typically due on April 15 each year."
},
{
    "id": 99,
    "question": "When must all men register for the Selective Service?",
    "options": [
        "At age 16",
        "At age 18",
        "Before age 21",
        "At age 25"
    ],
    "answer": "At age 18",
    "explanation": "Men between the ages of 18 and 25 are required to register with the Selective Service."
},
{
    "id": 100,
    "question": "What is freedom of religion?",
    "options": [
        "You can practice any religion or not practice a religion.",
        "The government can force you to practice a religion.",
        "You must attend church every week.",
        "Religious practice is forbidden."
    ],
    "answer": "You can practice any religion or not practice a religion.",
    "explanation": "Freedom of religion is guaranteed by the First Amendment, allowing individuals to follow or reject any faith."
}
    
]

@app.route("/")
def index():
    """Pagina iniziale del quiz"""
    session.clear()
    session['current_question'] = 0  # Zero-based index
    session['score'] = 0
    session['answers'] = []
    return render_template("index.html", questions=questions)

@app.route("/question/<int:question_id>")
def show_question(question_id):
    """Mostra una specifica domanda del quiz"""
    question_index = question_id - 1  # Convert to zero-based
    
    if question_index < 0 or question_index >= len(questions):
        return redirect(url_for('index'))
    
    session['current_question'] = question_index
    question_data = questions[question_index]
    
    return render_template(
        "question.html",
        question=question_data,
        question_number=question_id,  # 1-based for display
        total_questions=len(questions)
    )

@app.route("/submit", methods=["POST"])
def submit_answer():
    """Processa la risposta e passa alla prossima domanda o al risultato"""
    if 'current_question' not in session:
        return redirect(url_for('index'))
    
    current_index = session['current_question']
    selected_option = request.form.get('selected_option')
    
    # Verifica risposta
    is_correct = selected_option == questions[current_index]['answer']
    
    # Aggiorna punteggio
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    # Salva risposta
    session['answers'] = session.get('answers', [])
    session['answers'].append({
        'question_id': questions[current_index]['id'],
        'selected': selected_option,
        'correct': questions[current_index]['answer'],
        'is_correct': is_correct,
        'explanation': questions[current_index].get('explanation', '')
    })
    
    # Determina prossima azione
    if current_index >= len(questions) - 1:  # Ultima domanda
        return redirect(url_for('show_result'))
    else:
        next_question_id = current_index + 2  # 1-based ID
        return redirect(url_for('show_question', question_id=next_question_id))

@app.route("/result")
def show_result():
    """Mostra i risultati del quiz"""
    if 'score' not in session:
        return redirect(url_for('index'))
    
    return render_template(
        "result.html",
        score=session.get('score', 0),
        total=len(questions),
        answers=session.get('answers', []),
        questions=questions
    )

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve i file statici"""
    return send_from_directory('static', filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
