# Asynchronous Python Web Scraping Framework & Server

This project is a robust, fully asynchronous web scraping framework built with Python, aimed at providing a fast and efficient web scraping solution. The design takes inspiration from Scrapy, offering a structured approach to building web spiders and data processing pipelines.

## 🚀 Features

- **Fully Asynchronous**: Speed up your scraping tasks with non-blocking operations.
- **Modular Design**: Create spiders and pipelines using base classes for a consistent and maintainable structure.
- **Flexible Database**: Leveraging Tortoise-ORM with Postgresql, though it's designed for easy DBMS transitions.
- **Secure Authentication**: Client requests are authenticated using custom HTTP headers (API KEY and ACCESS ID) for enhanced security.

## 🛠️ Tech Stack

- **Server**: FastAPI and asyncio for asynchronous server operations.
- **Database**: Tortoise-ORM with Postgresql.
- **Web Scraping**: Spiders developed using aiohttp & playwright.
- **Data Parsing**: BeautifulSoup for parsing web content.

## 🕷️ How it Works

1. **Spiders**: Build spider objects by inheriting from the base Spider class.
2. **Pipelines**: Construct pipeline objects using the base Pipeline class.
3. **SpiderLauncher**: This class is responsible for launching the spiders, which asynchronously yield scraped data.
4. **Async Queue**: The yielded data is queued asynchronously, ready for pipelining.
5. **Pipeline Listener**: Processes queued data, invoking the appropriate pipeline module to handle data processing and storage.

For client interactions, a separate CLI application is used to launch spiders, view their details, and check their states (active/inactive).

## 🔒 Security

Authentication is managed using custom HTTP headers. Both API KEY and ACCESS ID are encrypted and stored in a PyNaCl "SecretBox" on the client side, accessed via the CLI app for enhanced security.

## 🚧 Project Status

This project is currently a work-in-progress. It was originally designed as a framework for skiptracing. However, its modular and asynchronous nature makes it an excellent starting point for anyone looking to build or expand upon a web scraping framework.