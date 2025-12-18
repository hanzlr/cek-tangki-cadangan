from flask import Flask, render_template, request
import math

app = Flask(__name__)

def cek_tangki_cadangan(max_km, rasio, kapasitas, alasan_ops):
    alasan = []
    confidence = 0

    kemampuan = kapasitas * rasio
    rekomendasi_liter = 0

    # 1. Alasan operasional (bobot tertinggi)
    if alasan_ops != "Tidak Ada":
        alasan.append(f"Pertimbangan operasional: {alasan_ops}")
        confidence += 40

    # 2. Perhitungan teknis
    if max_km > kemampuan:
        alasan.append("Jarak maksimum melebihi kemampuan tanki")
        confidence += 30

        kekurangan_km = max_km - kemampuan
        rekomendasi_liter = kekurangan_km / rasio

    if max_km > 0.8 * kemampuan:
        alasan.append("Jarak mendekati batas kemampuan tanki")
        confidence += 20

    if rasio < 5:
        alasan.append("Rasio boros")
        confidence += 10

    # Keputusan
    if confidence >= 50:
        keputusan = "BUTUH"
        rekomendasi_liter = (
            math.ceil(rekomendasi_liter / 10) * 10
            if rekomendasi_liter > 0 else 10
        )
    else:
        keputusan = "TIDAK"
        confidence = 100 - confidence
        rekomendasi_liter = 0
        alasan.append("Masih aman dengan tanki bawaan")

    return keputusan, "; ".join(alasan), kemampuan, rekomendasi_liter, confidence


@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None

    if request.method == "POST":
        try:
            max_km = float(request.form["max_km"])
            rasio = float(request.form["rasio"])
            kapasitas = float(request.form["kapasitas"])
            alasan_ops = request.form["alasan_ops"]

            keputusan, alasan, kemampuan, rekomendasi, confidence = cek_tangki_cadangan(
                max_km, rasio, kapasitas, alasan_ops
            )

            hasil = {
                "keputusan": keputusan,
                "alasan": alasan,
                "kemampuan": round(kemampuan, 2),
                "rekomendasi": rekomendasi,
                "confidence": confidence
            }

        except Exception:
            hasil = {
                "keputusan": "ERROR",
                "alasan": "Input tidak valid",
                "kemampuan": "-",
                "rekomendasi": "-",
                "confidence": "-"
            }

    return render_template("index.html", hasil=hasil)


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
