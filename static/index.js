const addDictBtn = document.getElementById('add-dictionary-button')
const header = document.getElementsByClassName('header')[0]
const modal = document.getElementById('pop')
const modalCloseBtn = document.getElementsByClassName('close')[0]
const delWordBtns = document.getElementsByClassName('delete-word')
const dictDelBtn = document.getElementsByClassName('delete-dictionary-button')
const searchBtn = document.getElementById('search-btn')
const addWordBtn = document.getElementById('add-word')
const spinner = document.getElementById('spinner')
const dictSelector = document.getElementById('dictionary_id')

let translation = {}
let selectDictId = dictSelector?.value

dictSelector?.addEventListener('change', function () {
  selectDictId = this.value
  translation.dictionary_id = selectDictId
})

for (var i = 0; i < delWordBtns.length; i++) {
  delWordBtns[i].addEventListener('click', function () {
    var wordId = this.getAttribute('data-word-id')
    spinner.style.display = 'flex'
    fetch('/delete', {
      method: 'POST',
      body: JSON.stringify({ word_id: wordId }),
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert('Kelime silindi')
          window.location.reload()
        } else {
          alert('Kelime silinirken hata oluştu.')
        }
        spinner.style.display = 'none'
      })
  })
}

header?.addEventListener('click', function () {
  window.location.href = '/'
})

for (var i = 0; i < dictDelBtn.length; i++) {
  dictDelBtn[i].addEventListener('click', function () {
    var dictId = this.getAttribute('data-dict-id')
    spinner.style.display = 'flex'
    fetch('/dict/delete', {
      method: 'POST',
      body: JSON.stringify({ dict_id: dictId }),
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert('Sözlük silindi')
          window.location.href = '/'
        } else {
          alert('Sözlük silinirken hata oluştu.')
        }
      })
      .catch((error) => {
        console.error('Sözlük silinirken hata oluştu.', error)
      })
      .finally(() => {
        spinner.style.display = 'none'
      })
  })
}

searchBtn?.addEventListener('click', function () {
  spinner.style.display = 'flex'
  var searchInput = document.getElementById('search').value
  var language = document.getElementsByClassName('language-dropdown')[0].value
  var kelime = document.getElementById('kelime')
  var anlam = document.getElementById('anlami')
  var result = document.getElementsByClassName('result')[0]

  if (searchInput) {
    spinner.style.display = 'flex'
    fetch('/search', {
      method: 'POST',
      body: JSON.stringify({ word: searchInput, language: language }),
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data) {
          result.style.display = 'block'
          kelime.innerHTML = searchInput
          anlam.innerHTML = data.translatedText

          translation = {
            source_language: data.detectedSourceLanguage
              ? data.detectedSourceLanguage
              : 'auto',
            source_text: data.input,
            target_text: data.translatedText ? data.translatedText : 'xxx',
            target_language: language,
            dictionary_id: selectDictId,
          }
        } else {
          alert('Arama yapılırken hata oluştu.')
        }
      })
      .catch((error) => {
        console.error('Arama yapılırken hata oluştu.', error)
      })
      .finally(() => {
        spinner.style.display = 'none'
      })
  }
})

addWordBtn?.addEventListener('click', function () {
  spinner.style.display = 'flex'

  if (selectDictId) {
    fetch('/create', {
      method: 'POST',
      body: JSON.stringify(translation),
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert('Kelime eklendi.')
          window.location.reload()
        } else {
          alert('Kelime zaten var !!!')
        }
      })

      .catch((error) => {
        console.error('Kelime eklenirken hata oluştu.', error)
      })
      .then(() => {
        spinner.style.display = 'none'
      })
  } else {
    alert('Sözlük seçiniz.')
    spinner.style.display = 'none'
  }
})

modalCloseBtn.addEventListener('click', function () {
  modal.style.display = 'none'
})

addDictBtn.addEventListener('click', function () {
  modal.style.display = 'flex'
})

//document
//  .getElementById('submit-dictionary-button')
//  .addEventListener('click', function () {
//    var dictionaryName = document.getElementById('dictionary-name').value
//    if (dictionaryName) {
//      var dictionaryList = document.getElementById('dictionary-list')
//      var existingDictionaries = dictionaryList.getElementsByTagName('a')
//      for (var i = 0; i < existingDictionaries.length; i++) {
//        if (existingDictionaries[i].textContent === dictionaryName) {
//          document.getElementById('alert-box').textContent =
//            'Bu sözlük zaten var !!!'
//          document.getElementById('alert-box').style.display = 'block'
//          return
//        }
//      }
//      var newListItem = document.createElement('li')
//      var newLink = document.createElement('a')
//      newLink.href = '#'
//      newLink.textContent = dictionaryName
//      newListItem.appendChild(newLink)
//      dictionaryList.appendChild(newListItem)
//      document.getElementById('add-dictionary-form').style.display = 'none'
//      document.getElementById('dictionary-name').value = '' // Sözlük eklenince adı temizlenir
//      document.getElementById('alert-box').style.display = 'none' // Sözlük eklendiğinde mesajı kapatır
//    }
//  })
//
//// error message box
//document.addEventListener('DOMContentLoaded', function () {
//  const errorMessageBox = document.getElementById('error-message-box')
//  const errorMessageText = document.getElementById('error-message-text')
//  const closeErrorBox = document.getElementById('close-error-box')
//
//  if ('{{ error_message }}' !== 'None') {
//    errorMessageText.textContent = '{{ error_message }}'
//    errorMessageBox.style.display = 'block'
//  }
//
//  closeErrorBox.addEventListener('click', function () {
//    errorMessageBox.style.display = 'none'
//  })
//})
//
//// sözlükleri alma
//document.addEventListener('DOMContentLoaded', function () {
//  fetch('/get-dictionaries') // İsmi güncelle !!!
//    .then((response) => response.json())
//    .then((data) => {
//      const dictionaryList = document.getElementById('dictionary-list')
//
//      dictionaryList.innerHTML = ''
//
//      data.dictionaries.forEach((dictionary) => {
//        const newListItem = document.createElement('li')
//        const newLink = document.createElement('a')
//        newLink.href = '#'
//        newLink.textContent = dictionary
//        newListItem.appendChild(newLink)
//        dictionaryList.appendChild(newListItem)
//      })
//    })
//    .catch((error) => {
//      console.error('Sözlükler alınırken hata oluştu.', error)
//    })
//})
//
