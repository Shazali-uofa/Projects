from pymongo import MongoClient
import re
import sys


if len(sys.argv) != 2:
    print("Usage: python3 phase2_query.py <port>")
    sys.exit(1)

port=sys.argv[1]

# Connecting to the local host
client = MongoClient(f"mongodb://localhost:{port}")
# This will tell us which database to use
db=client["291db"]

def UserOptions():
    print("\n============ 📊 USER MENU =================\n")
    print("[C] → Common Words (Top 5)\n")
    print("[A] → Article Count (News vs Blogs)\n")
    print("[S] → Article Sources in 2015\n")
    print("[M] → Most Recent Articles by Source\n")
    print("[Q] → Quit\n")
    print("=============================================\n")

    while True:

        option=input("👉 Choose an option: ").strip().lower()
        # If user types in c option then we direct him to common words function
        if option=="c":
            print("\n🔍 Opening Common Words...\n")
            Common_words()

        # If the user types in a take him to article count funciton
        elif option=="a":
            print("📰 Article Count...\n")
            Article_Count()

        # If the user types in s we take him to the following function
        elif option=="s":
            News_Sources()
            

        elif option=="m":
            print("📰 most recent...\n")
            Most_Recent_Articles()

        
        elif option=="q":
            print("👋 Exiting the program. Bye bye!")
            break

        else:
            print("❌ Invalid option! Please choose again.\n")

# This is used for the top 5 words
def Common_words():
    user_input = input("📝 Enter media type (news/blog): ").strip().lower()
    
    if user_input not in ["news", "blog"]:
        print("❌ Invalid media type. Please enter 'news' or 'blog'.")
        return
    
    print(f"🔍 Showing top words for: {user_input}\n")

    # $options:i ignores all the capital/lowercase difference 
    cursor=db.articles.find(

        {"media-type": {"$regex": f"^{user_input}$", "$options": "i"}},
        {"media-type":True,"_id":False,"content":True}
    )
    

    dic={}
    for results in cursor:

        content=results["content"]
        lower = re.sub(r"[^A-Za-z0-9_-]", " ", content.lower()).split()

        for w in lower:
            if w in dic:
                dic[w]+=1
            else:
                dic[w]=1

    arr = [(v, k) for k, v in dic.items()]

    sorted_arr=sorted(arr,reverse=True)

    # If the array was empty just return it
    if len(sorted_arr)==0:
        print("No words found")
        return
    
    # If the lenght of sorted_arr then the cutoff is the 5th word count
    if len(sorted_arr) >= 5:
        cutoff = sorted_arr[4][0]
    # If not then its the last element word count   
    else:
        cutoff = sorted_arr[-1][0]

    
    print("📊 Top 5 most common words:")
    
    for count, word in sorted_arr:
        if count >= cutoff:
            print(f"{word:<20} {count}")

# This function is used for Article Count

def Article_Count():

    date_input = input("📅 Enter date (YYYY-MM-DD): ").strip()

    cursor=db.articles.find({
        "published": {
            "$regex":f"^{date_input}T"
        }
    },{"published":True,"media-type":True,"_id":False})

    news_count=0
    blog_count=0

    for results in cursor:
        media=results["media-type"].lower()

        if media=="news":
            news_count+=1
        elif media=="blog":
            blog_count+=1

    total=news_count+blog_count

    if total==0:
        print("❌ No articles were published on this day.")
        return
    
    print("\n📊 Article Count Results")
    print("News:", news_count)
    print("Blog:", blog_count)

    # Compare which is more
    if news_count>blog_count:
        print(f"📰 More NEWS by {news_count - blog_count}")

    elif blog_count > news_count:
        print(f"✍️ More BLOGS by {blog_count - news_count}")

    else:
        print("⚖️ Same number of News and Blogs")

def News_Sources():
    
    sources = [
        {"$match": {
            "media-type":{"$regex":"^news$","$options":"i"},
            "published": {"$gte": "2015-01-01", "$lt": "2016-01-01"}
        }},
        {"$group": {
            "_id": "$source",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    results = list(db.articles.aggregate(sources))
    # If the results are not found TO BE IMPROVED
    if not results:
        print("❌ No news articles found for 2015.")
        return

    if len(results)>=5:
        cutoff=results[4]["count"]
    else:
        cutoff=results[-1]["count"]

    print("Top 5 news sources in 2015 by article count:")
    for r in results:
        if r["count"]>=cutoff:
            print(f"{r['_id']:<30} {r['count']}")


def Most_Recent_Articles():
    
    source_input = input("📝 Enter news source: ").strip().lower()
    print(f"🔍 Fetching most recent articles from: {source_input}\n")

    # Get all articles for that source (case-insensitive)
    all_articles = list(db.articles.find(
        {"source": {"$regex": f"^{source_input}$", "$options": "i"}},
        {"title": 1, "published": 1, "_id": 0}
    ).sort("published", -1))

    if len(all_articles)==0:
        print("❌ Source not found.")
        return
    
    print(f"\n📰 Most recent articles from {source_input}:\n")

    # For less than 5 articles
    if len(all_articles) <= 5:
        print(f"📰 Articles from {source_input}:")
        for article in all_articles:
            date = article["published"].split("T")[0]
            print(f"Title: {article['title']}  Date: {date}")
        return

    cutoff_date=all_articles[4]["published"].split("T")[0]
        
    # If more than 5 → show only top 5
    for article in all_articles:
        article_date=article["published"].split("T")[0]
        if article_date>=cutoff_date:
            print(f"Title: {article['title']}  Date: {article_date}")


if __name__=="__main__":
    UserOptions()

client.close()