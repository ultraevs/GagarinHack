export default function nameEncoder(str, page_number) {
  if (str === "vehicle_passport") {
    return "ПТС";
  } else if (str === "personal_passport" && page_number === "1") {
    return "Паспорт стр. 1";
  }
  else if (str === "personal_passport" && page_number === "2") {
    return "Паспорт стр. 2";
  } else if (str === "vehicle_certificate" && page_number === "1") {
    return "СТС стр. 1";
  }
  else if (str === "vehicle_certificate" && page_number === "2") {
  return "СТС стр. 2";
  } 
  else if (str === "driver_license" && page_number === "1"){
    return "В/У стр. 1";
  }
  else if (str === "driver_license" && page_number === "2"){
    return "В/У стр. 2"
  }
}
