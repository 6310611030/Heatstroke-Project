if('serviceWorker' in navigator){
    navigator.serviceWorker.register("service-worker.js").then(reg => {
      console.log(`Registration:`, reg);
    }).catch(err => {
      console.warn(`Registration:`, err);
    })
  }