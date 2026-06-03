console.log("JS cargado");
function switchFloor(floor) {
    const p1 = document.getElementById('map-piso-1');
    const pm1 = document.getElementById('map-piso-minus-1');
    const title = document.getElementById('floor-subtitle');
    const tag = document.getElementById('floor-tag');

    if (floor === -1) {
        p1.classList.add('hidden');
        pm1.classList.remove('hidden');
        title.innerText = "Ubicación: Piso -1 ";
        tag.innerText = "Nivel Inferior";
        tag.className = "bg-slate-700 px-4 py-2 rounded-lg text-xs font-bold border border-slate-600 uppercase";
    } else {
        pm1.classList.add('hidden');
        p1.classList.remove('hidden');
        title.innerText = "Ubicación: Piso 1";
        tag.innerText = "Nivel Principal";
        tag.className = "bg-blue-800 px-4 py-2 rounded-lg text-xs font-bold border border-blue-700 uppercase";
    }
}