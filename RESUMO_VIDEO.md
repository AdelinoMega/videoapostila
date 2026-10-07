# Vídeo promocional — Apostila MegaDJ (9:16)

## Entregáveis
- `video_completo_1080x1920.mp4` — montagem 22,75s (6 clipes, fusões de 0,25s), 1080x1920, sem áudio
- `clip01_capa.mp4` … `clip06_final.mp4` — clipes individuais 720x1280, 4s cada, 24 fps, sem áudio

## Método (fidelidade)
1. Quadros-base gerados com `gen4_image` (mesa, MacBook, fones) com páginas EM BRANCO.
2. Páginas reais do PDF aplicadas por cima em perspectiva (luz/sombra transferidas da página em branco).
3. Vídeo com `veo3.1` (sem áudio) usando primeiro E último quadro = páginas reais, então cada clipe começa e termina em páginas verdadeiras.

## Clipes
| Clipe | Duração | Páginas reais | Movimento |
|---|---|---|---|
| 01 Capa | 4s | 1 (capa) | push-in lento |
| 02 Abrindo | 4s | 1 → 2 + 3 | mão abre a capa |
| 03 Folheando | 4s | 2 + 3 → 6 + 14 | 1 folha virada |
| 04 Apostila + Serato | 4s | 68 + 102 | mão no trackpad, rack focus |
| 05 Conteúdo técnico | 4s | 50 + 137 → 14 + 95 (Camelot) | mais perto, 1 folha virada |
| 06 Final | 4s | 14 + 95 | pull-back, sem mãos |

Obs.: as páginas duplas combinam páginas reais que não são vizinhas no PDF (os números de página são ilegíveis no vídeo). A página 14 aparece nos clipes 03, 05 e 06.

## Regenerados
- Clip 02 (v1 tinha salto de corte e capa translúcida) — refeito com livro fechado na mesma posição.
- Clip 03 (v1 inventou uma página intermediária e mostrou verso em branco) — refeito com o verso descrito.
Versões rejeitadas em `rejeitados/`.

## Limitações conhecidas
- Tela do MacBook: software de DJ genérico, não a interface real do Serato DJ Pro (desfocado, só contexto).
- Durante a virada de folha, o papel em movimento fica borrado (sem conteúdo legível inventado).
- Upscale para 1080x1920 feito com ffmpeg (lanczos), não com IA.

## Créditos Runway
Gastos: ~690 (imagens 35, prévia gen4_turbo 15, vídeos veo3.1 640). Saldo: 310.

## Ordem de edição
01 → 02 → 03 → 04 → 05 → 06
