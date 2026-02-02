# QR Code Service API

A FastAPI-based microservice for generating customized QR codes with logos, shapes, and color customization.

## Features

- **Custom Shapes**: Generate QR codes with heart, circle, or default square modules
- **Color Customization**: Set custom foreground and background colors
- **Logo Embedding**: Add logos to the center of QR codes
- **Error Correction**: Configurable error correction levels (L, M, Q, H)
- **Scalability**: Dockerized for easy deployment
- **RESTful API**: Simple HTTP endpoint for QR generation

---

## Table of Contents

- [Installation](#installation)
  - [Docker Setup](#docker-setup)
- [API Usage](#api-usage)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Docker Setup

2. **Run the container**
   ```bash
   docker run -p 8000:8000 qr-code-service
   ```

---

## API Usage

### Endpoint

**POST** `/generate_qr`

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | string | ✅ | - | Content to encode in QR code (URL, text, etc.) |
| `foreground` | string | ❌ | `black` | QR module color (see [Color Formats](#color-formats)) |
| `background` | string | ❌ | `white` | Background color (see [Color Formats](#color-formats)) |
| `scale` | integer | ❌ | `5` | Size scaling factor (pixels per module) |
| `shape` | string | ❌ | `default` | Module shape: `default`, `heart`, `circle` |
| `shape_scale` | float | ❌ | `1.3` | Shape size multiplier |
| `error_level` | string | ❌ | `h` | Error correction: `l`, `m`, `q`, `h` |
| `logo_image` | file | ❌ | `null` | Logo image file (PNG/JPG) |
| `logo_scale` | float | ❌ | `0.2` | Logo size as fraction of QR width (0.0-1.0) |

### Color Formats

Both `foreground` and `background` parameters accept multiple color formats:

| Format | Example | Description |
|--------|---------|-------------|
| **Hex** | `#FF0000`, `#f00` | Standard hexadecimal color codes |
| **RGB** | `rgb(255, 0, 0)` | RGB color values |
| **RGBA** | `rgba(255, 0, 0, 0.5)` | RGB with transparency (alpha) |
| **Named Colors** | `red`, `blue`, `black`, `white` | Standard CSS color names |

**Color Guidelines:**
- **Foreground**: The color of the QR code modules (dark parts)
- **Background**: The color behind the QR code (light parts)

### Response

Returns a PNG image stream with `Content-Type: image/png`

---

## Examples

### 1. Basic QR Code

```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=https://example.com" \
  -o qr_basic.png
```

### 2. Colored Heart-Shaped QR

```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=https://bracuniversity.edu" \
  -F "foreground=#FF0000" \
  -F "background=#FFFF00" \
  -F "shape=heart" \
  -F "scale=10" \
  -o qr_heart.png
```

### 3. QR with Logo

```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=BRAC University" \
  -F "logo_image=@logos/bracu.png" \
  -F "logo_scale=0.25" \
  -F "error_level=h" \
  -o qr_logo.png
```

### 4. Circle-Shaped Blue QR

```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=Custom Design QR" \
  -F "foreground=#1E40AF" \
  -F "shape=circle" \
  -F "shape_scale=1.5" \
  -o qr_circle.png
```

### 5. Color Variations

**Using Named Colors:**
```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=https://example.com" \
  -F "foreground=darkblue" \
  -F "background=lightgray" \
  -o qr_named_colors.png
```

**Using RGB Format:**
```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=https://example.com" \
  -F "foreground=rgb(139, 0, 0)" \
  -F "background=rgb(255, 250, 205)" \
  -o qr_rgb.png
```

**High Contrast (Best for Scanning):**
```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=https://example.com" \
  -F "foreground=#000000" \
  -F "background=#FFFFFF" \
  -o qr_high_contrast.png
```

**Brand Colors Example:**
```bash
curl -X POST "http://localhost:8000/generate_qr" \
  -F "data=https://bracuniversity.edu" \
  -F "foreground=#003366" \
  -F "background=#F0F0F0" \
  -F "shape=circle" \
  -o qr_brand.png
```



---

## Configuration

### Error Correction Levels

| Level | Correction Capacity | Use Case |
|-------|---------------------|----------|
| `l` | ~7% | Clean environments, maximum data capacity |
| `m` | ~15% | Standard use cases |
| `q` | ~25% | Recommended for most applications |
| `h` | ~30% | Best for logos or damaged/dirty environments |

### Recommended Settings

**For QR codes with logos:**
- Use `error_level=h` (highest correction)
- Keep `logo_scale` between `0.15-0.25`
- Larger logos may prevent scanning
- Test scanning before production use

**For artistic/shaped QR codes:**
- Use `shape_scale=1.3-1.5` for better module coverage
- Maintain high contrast between foreground/background
- Avoid very light colors for foreground
- Test with multiple QR scanners

---

## Troubleshooting

### Common Issues

**Issue**: QR code won't scan
- **Solution**: 
  - Increase `error_level` to `h`
  - Reduce `logo_scale` (try 0.15-0.20)
  - Increase `scale` for larger output
  - Ensure high contrast between colors

---

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- QR generation powered by [segno](https://segno.readthedocs.io/)
- Shape rendering using [CairoSVG](https://cairosvg.org/)
- Image processing with [Pillow](https://pillow.readthedocs.io/)

---

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: sakibulhaque2002

---