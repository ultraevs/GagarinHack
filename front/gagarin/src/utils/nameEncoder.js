export default function nameEncoder(str, page_number) {
  if (str === "vehicle_passport") {
    return "ПТС";
  } else if (str === "personal_passport" && page_number === "1") {
    return "Паспорт страница 1";
  }
  else if (str === "personal_passport" && page_number === "2") {
    return "Паспорт страница 2";
  } else if (str === "vehicle_certificate" && page_number === "1") {
    return "СТС страница 1";
  }
  else if (str === "vehicle_certificate" && page_number === "2") {
  return "СТС страница 2";
  } 
  else if (str === "driver_license" && page_number === "1"){
    return "В/У страница 1";
  }
  else if (str === "driver_license" && page_number === "2"){
    return "В/У страница 2"
  }
}
