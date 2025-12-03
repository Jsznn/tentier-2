# Tutorial Export & Save Model (ML & Deep Learning)

Dokumen ini berisi panduan cara menyimpan (export) dan memuat kembali (load) model Machine Learning dan Deep Learning menggunakan berbagai framework populer.

## 1. Scikit-Learn
Untuk model tradisional seperti Linear Regression, Random Forest, SVM, dll.

### Menggunakan `joblib` (Direkomendasikan)
`joblib` lebih efisien untuk objek yang membawa array numpy besar.

**Install:**
```bash
pip install joblib
```

**Save:**
```python
import joblib

# Anggap 'model' adalah model sklearn yang sudah dilatih
joblib.dump(model, 'model_filename.pkl')
```

**Load:**
```python
import joblib

model = joblib.load('model_filename.pkl')
result = model.predict(X_test)
```

### Menggunakan `pickle` (Standard Python)
**Save:**
```python
import pickle

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

**Load:**
```python
import pickle

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
```

---

## 2. TensorFlow / Keras
Untuk model Deep Learning berbasis TensorFlow.

### Format `.keras` (Format Standar Baru - TF 2.x)
Ini adalah format modern yang direkomendasikan.

**Save:**
```python
model.save('my_model.keras')
```

**Load:**
```python
from tensorflow.keras.models import load_model

model = load_model('my_model.keras')
```

### Format `.h5` (Legacy)
Format HDF5 yang lama.

**Save:**
```python
model.save('my_model.h5')
```

### Format `SavedModel` (Untuk TensorFlow Serving)
Menyimpan model sebagai direktori berisi protobuf dan variabel. Cocok untuk deployment production.

**Save:**
```python
model.export('path/to/saved_model')
# Atau
tf.saved_model.save(model, 'path/to/saved_model')
```

---

## 3. PyTorch
Untuk model Deep Learning berbasis PyTorch.

### Menyimpan `state_dict` (Direkomendasikan)
Hanya menyimpan parameter (bobot) model. Lebih fleksibel dan aman.

**Save:**
```python
import torch

torch.save(model.state_dict(), 'model_weights.pth')
```

**Load:**
Anda harus mendefinisikan arsitektur model terlebih dahulu.
```python
model = MyModelClass(*args, **kwargs)
model.load_state_dict(torch.load('model_weights.pth'))
model.eval() # Jangan lupa set ke mode evaluasi untuk inferensi
```

### Menyimpan Seluruh Model
Menyimpan struktur kelas dan bobot. Bisa bermasalah jika struktur direktori kode berubah.

**Save:**
```python
torch.save(model, 'entire_model.pth')
```

**Load:**
```python
model = torch.load('entire_model.pth')
model.eval()
```

---

## 4. Format Interoperabilitas (ONNX)
Open Neural Network Exchange (ONNX) memungkinkan model dijalankan di berbagai framework dan hardware (misal: convert PyTorch ke ONNX untuk dijalankan di C++ atau Web).

### Scikit-learn ke ONNX
Butuh library `skl2onnx`.

```python
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

initial_type = [('float_input', FloatTensorType([None, 4]))]
onx = convert_sklearn(model, initial_types=initial_type)
with open("model.onnx", "wb") as f:
    f.write(onx.SerializeToString())
```

### PyTorch ke ONNX
```python
dummy_input = torch.randn(1, 3, 224, 224) # Sesuaikan dengan input shape
torch.onnx.export(model, dummy_input, "model.onnx")
```

---

## 5. Tips Tambahan

1.  **Versioning**: Selalu beri versi pada nama file model atau folder (contoh: `model_v1.0.pkl` atau `models/2023-10-27/`).
2.  **Metadata**: Simpan metadata pelatihan (akurasi, parameter, tanggal training) dalam file JSON terpisah atau dictionary bersama model (jika menggunakan pickle/joblib).
3.  **Environment**: Catat versi library (`requirements.txt`) saat training. Model yang dilatih di scikit-learn versi lama mungkin error jika di-load di versi baru.
