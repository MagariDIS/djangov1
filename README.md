---
title: Django
description: A Django application that connects to a PostgreSQL database
tags:
  - python
  - django
  - postgresql
---

# Django Example

This is a [Django](https://www.djangoproject.com/) application that connects to a Railway Postgres database.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?template=https%3A%2F%2Fgithub.com%2Frailwayapp%2Fexamples%2Ftree%2Fmaster%2Fexamples%2Fdjangopy&plugins=postgresql&envs=SECRET_KEY&SECRET_KEYDesc=Django+secret+key+used+for+authentication)

## ✨ Features

- Python
- Django
- Postgres

## 💁‍♀️ How to use

- [Create a Railway project with the Postgres plugin](https://railway.app/project?plugins=postgresql)
- Connect to your Railway project with `railway link`
- Install Python requirements `pip install -r requirements.txt`
- Migrate the database `railway run python3 manage.py migrate`
- Run Django `railway run python3 manage.py runserver`

## 📝 Notes

Read more about Django at their [official
documentation](https://www.djangoproject.com/start/).

[django_cerery_redisによる非同期処理の実装/](https://zats-firm.com/2022/02/05/django_cerery_redisによる非同期処理の実装/)


## G

このコースでは、非同期処理(Celery)を備えたDjangoスクレイピングアプリをGCEで公開するやり方を説明しています。 All the course is for about 3 hours and divided to 14 part. このコースは全部で約3時間あり、14のパートから構成されております。 
【PART1】 url : [https://youtu.be/Ow-oaFBYOVE](https://www.youtube.com/watch?v=Ow-oaFBYOVE&t=0s) Describes about what you'll learn. パート1ではコースの概要を説明しています。 

【PART2】 url : [https://youtu.be/8YrEamScS5A](https://www.youtube.com/watch?v=8YrEamScS5A&t=0s) Describes about how create Django app. パート2ではDjangoアプリを作成します。

【PART3】 url : [https://youtu.be/FYa88b8Fkpg](https://www.youtube.com/watch?v=FYa88b8Fkpg&t=0s) Describes about how to use Django form with html. パート3ではDjangoフォームの使い方とHTMLを調整します。 

【PART4】 url : [https://youtu.be/ReZhVVJGQsQ](https://www.youtube.com/watch?v=ReZhVVJGQsQ&t=0s) Describes about how to use Django Class Based Vies. パート4ではDjangoのクラスベースドビューの使い方を説明します。 

【PART5】 url : [https://youtu.be/bQp8oBKiRGE](https://www.youtube.com/watch?v=bQp8oBKiRGE&t=0s) Describes about how to create scraping function. パート5ではスクレイピング機能を追加します。 

【PART6】 url : [https://youtu.be/8OPpe4nFxy0](https://www.youtube.com/watch?v=8OPpe4nFxy0&t=0s) Describes about how to save scraped data on GCS(Google Cloud Storage) パート6ではスクレイピングで取得したデータをGCSへ保存します。 

【PART7】 url : [https://youtu.be/Aeo4qXaAOgY](https://www.youtube.com/watch?v=Aeo4qXaAOgY&t=0s) Describes about how to save scraped data with UUID(Universally Unique Identifier) パート7ではスクレイピングで取得したデータをユニークIDを使って、保存します。 

【PART8】 url : [https://youtu.be/aR-OpuiWVkU](https://www.youtube.com/watch?v=aR-OpuiWVkU&t=0s) Describes about how to download scraped data パート8ではスクレイピングで取得したデータのダウンロード方法を説明します。 

【PART9】 url : [https://youtu.be/UvL-L0w83Sw](https://www.youtube.com/watch?v=UvL-L0w83Sw&t=0s) Describes about how to create Celery settings. パート9ではCeleryの設定方法を説明します。 

【PART10】 url : [https://youtu.be/XpTKar3EWgE](https://www.youtube.com/watch?v=XpTKar3EWgE&t=0s) Describes about how to use Celery processing. パート10ではCeleryでの非同期処理方法を説明します。 

【PART11】 url : [https://youtu.be/bKfIEhC-4yk](https://www.youtube.com/watch?v=bKfIEhC-4yk&t=0s) Describes about how to use Gmail API to send email. パート11ではGmail APIの説明をします。 

【PART12】 url : [https://youtu.be/xEK3sK80phk](https://www.youtube.com/watch?v=xEK3sK80phk&t=0s) Describes about how to create github repository and GCE(Google Compute Engine) instance. パート12ではgithubリポジトリ＆GCEインスタンスの作成方法を説明します。 

【PART13】 url : [https://youtu.be/hfyC9e1uab4](https://www.youtube.com/watch?v=hfyC9e1uab4&t=0s) Describes about how to install Python and other software on Ubuntu18.04 パート13ではGCEインスタンス内のUbuntuOS内で必要なPython環境＆その他ソフトウェアの準備を行います。 

【PART14】 url : [https://youtu.be/ACZZq5A6HHU](https://www.youtube.com/watch?v=ACZZq5A6HHU&t=0s) Describes about how to start Django app with Celery on GCE. パート14では作成した非同期スクレイピング処理機能を備えたDjangoアプリをGCEで起動し、 公開します。