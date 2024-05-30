from django.shortcuts import render

def test(r):
  return render(r, 'home.html')