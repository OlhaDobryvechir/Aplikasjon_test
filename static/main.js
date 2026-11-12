var temy;

function temArbeider(mova) {
        const temki = document.getElementById("temki");
        temki.innerHTML = "";
        const tem_kilkist = temy.length;
        for(let i = 0; i<tem_kilkist; i++) {
               const d = document.createElement("div");
               d.innerHTML = temy[i]["name_"+mova];
               temki.append(d);
        }
}

function readtema() {
     fetch ("/api/tema")
    .then(response => response.json())
    .then(data => {
         temy = data; temArbeider("en");
            })
    .catch(error => {

        console.error('Помилка:', error);
    });
}

function goto(siteUrl) {
    window.location.href=siteUrl;
}
function approveText(language) {
    const korobka = document.getElementById("name_"+language);
    const beforeValueCreate = korobka.value.trim();
    if (!beforeValueCreate) {
    korobka.style.border = "3px solid red ";
    } else {
    korobka.style.border = "2px solid green ";
    }

}

function createTema() {
    const korobochka_en = document.getElementById("name_en");
    const korobochka_no = document.getElementById("name_no");
    const english = korobochka_en.value.trim();
    const norwegian = korobochka_no.value.trim();
    if (!english) {
    korobochka_en.style.border = "3px solid red ";
    } else {
    korobochka_en.style.border = "2px solid green";
    }
    if (!norwegian) {
    korobochka_no.style.border = "3px solid red";
    } else {
    korobochka_no.style.border = "2px solid green";
    }
    if (!english || !norwegian) {
    return;
    }
    const temaUrl = "/api/tema";

const data = {

  name_en: english,
  name_no: norwegian
};

fetch(temaUrl, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(result => {
    console.log("Success:", result);
    goto("index.html");
  })
  .catch(error => {
    console.error("Error:", error);
  });
}
