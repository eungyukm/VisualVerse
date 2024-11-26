# Visual Verse
VisualVerse is an AI-powered bloggin platform that transforms your words into captivating visuals.
By analyzing your blog content, VisualVerse automatically generates unique cover images tailored to the essence of your writing.
Whether you're sharing personal stories, insights, or tutorials, VisualVerse ensures your posts stand out with a touch of creativity.


## Features
- **AI-Powered Analysis**: Automatically analyze blog content to understand the theme and mood.
- **Custom Cover Generation**: Create visually stunning and unique cover images for each post.
- **User-Friendly Interface**: Write, customize, and publish blogs effortlessly.
- **Scalbalbe Design**: Supports bloggers of all scales, from individuals to businesses.

## Why VisualVerse?
Blogging is more than just words. It's about presentation, creativity, and leaving an impression. VisualVerse enhances your blogging experience by bridging the gap between content and visuals, making your posts unforgettable.

## Getting Started
1. Clone the repository

## Django Project Code Convention
This document provides coding guidelines to maintain consistency and readbility across Django projects.

## 1. File and Directory Structure
- Use lowercase sigular names for app directories. ex) 'loginmanager', 'blog'
- Maintain the follwing directory structure for each app.

## 2. Follow the PEP 8 Style guide for Python code
- Indentation : Use 4 spaces per indentation level.
- Line length : Limit lines to 79 characters.
- Use 2 blank lines between top-level functions and classes.
- Use 1 blank line between method inside a class.

## 3. Models
3.1 Model Class
- Use PascalCase for model class names.
- Use lowercase_snake_case for field anmes.

3.2 Field Options
- Be explicit when defining field options, such as nuull, blank, and default.

4. Views
4.1 Function-Based Views (FBVs)
- Use lowercase_snake_case for function names.
- Separate complex logic into helper functions or classes for better readability.

4.2 Class-Based Views (CBVs)
- Use PascalCase for class names.
- Implement HTTP methods (get, post, etc.) as class methods.

5. URLs
- Use lowercae and hyphen-separdted patterns for URLs.
- Define app_name to avoide conflicts and use name for reverse URL lookups.

6. Templates
- Store templates in an app-specific directory under templates/
- Use lowercase and hyphen-separted names for templates.

