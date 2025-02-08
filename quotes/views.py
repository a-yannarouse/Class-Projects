from django.shortcuts import render
import random

quotes = ["Don't allow anybody to project any stereotypes on you that tell you that you can't be here—that you're too dark, that you're not smart enough, that you're too dramatic or too loud, she said. You are exactly who you need to be, to be right where you are, and I am a testimony.", 
          "However you want to define me, make the comparisons, but I'm going to continue to push and challenge what 'genre' means and what it is. I think music challenges that.",
          "I want to open as many doors as possible.",
          "Make a few bands and switch tribes, they switch sides…Only thing switchin on me, is thick thighs.",
          "Our music has always been deep…once we lost the soul we've lost the genre.",
          "This category was introduced in 1989, and two women have won--THREE women have won! Lauryn Hill, Cardi B., and Doechii!",
        ]
images = ["https://i.scdn.co/image/ab67616100005174ca2fee52c41d3f58ceb6474b", "https://www.rollingstone.com/wp-content/uploads/2024/09/doechii-interview-album.jpg?w=1581&h=1054&crop=1",
          "https://static01.nyt.com/images/2024/12/20/multimedia/20DOECHII-STYLE-03-hmpq/20DOECHII-STYLE-03-hmpq-articleLarge.jpg?quality=75&auto=webp&disable=upscale",
          "https://www.billboard.com/wp-content/uploads/2023/03/01-Doechii-2023-billboard-women-in-music-wim-show-billboard-1548.jpg?w=1024",
          "https://stupiddope.com/wp-content/uploads/2024/12/Doechii-Brings-Her-Dynamic-Sound-to-NPRs-Tiny-Desk-1875x1875.jpeg",
          "https://i0.wp.com/culturacolectiva.com/wp-content/uploads/2025/01/doechii.jpg?resize=1080%2C1350&ssl=1"
          ]
# Create your views here.
def home_page(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    context = {"quote": selected_quote, "image": selected_image}
    return render(request, "quotes/home.html", context)

def quote_page(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    context = {"quote": selected_quote, "image": selected_image}
    return render(request, "quotes/quote.html", context)

def about_page(request):
    return render(request, "quotes/about.html")

def show_all_page(request):
    context = {"quotes": quotes, "images": images}
    return render(request, "quotes/show_all.html", context)
