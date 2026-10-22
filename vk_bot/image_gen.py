from PIL import Image, ImageDraw, ImageFont


def create_structures_image(categories):
    """Создаёт изображение с таблицей структур и игроков."""
    padding, cell_padding = 20, 10
    header_height, row_height = 50, 30
    font_size, header_font_size = 13, 15

    structures = [name for name, data in categories.items() if data["members"]]
    if not structures:
        img = Image.new("RGB", (500, 200), color=(30, 30, 40))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except OSError:
            font = ImageFont.load_default()
        draw.text((20, 80), "Нет данных о структурах", fill=(255, 255, 255), font=font)
        return img

    max_members = max(len(d["members"]) for d in categories.values() if d["members"])
    num_rows = max(1, max_members + 1)
    column_width = 350
    img_width = len(structures) * (column_width + padding) + padding
    img_height = num_rows * row_height + header_height + padding * 2 + 50

    img = Image.new("RGB", (int(img_width), int(img_height)), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        header_font = ImageFont.truetype("arial.ttf", header_font_size)
        small_font = ImageFont.truetype("arial.ttf", font_size - 2)
    except OSError:
        font = header_font = small_font = ImageFont.load_default()

    draw.text((padding, 10), "📊 Структура армии", fill=(255, 255, 255), font=header_font)

    y = header_height + padding
    for col_idx, name in enumerate(structures):
        data = categories[name]
        x = padding + col_idx * (column_width + padding)

        header_text = f"{name}\n({data['max']} - {data['min']})"
        draw.rectangle([x, y, x + column_width, y + header_height], fill=(50, 50, 80))
        current_y = y + 5
        for line in header_text.split("\n"):
            bbox = draw.textbbox((0, 0), line, font=header_font)
            text_x = x + (column_width - (bbox[2] - bbox[0])) // 2
            draw.text((text_x, current_y), line, fill=(255, 255, 200), font=header_font)
            current_y += header_font_size + 3

        for row_idx, member in enumerate(data["members"]):
            row_y = y + header_height + row_idx * row_height
            color = (60, 60, 80) if row_idx % 2 == 0 else (45, 45, 65)
            draw.rectangle([x, row_y, x + column_width, row_y + row_height],
                           fill=color, outline=(100, 100, 130), width=1)
            text = " ".join(member.strip().replace("\n", " ").split())
            if len(text) > 45:
                text = text[:42] + "..."
            draw.text((x + cell_padding, row_y + 5), text, fill=(200, 200, 255), font=small_font)

    total = sum(len(d["members"]) for d in categories.values() if d["members"])
    stats_y = y + header_height + max_members * row_height + padding
    draw.text((padding, stats_y), f"📊 Всего людей на должностях: {total}",
              fill=(150, 200, 150), font=font)
    return img
