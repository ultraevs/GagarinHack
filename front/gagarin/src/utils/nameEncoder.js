export default function nameEncoder(str) {
  if (str === "vehicle_passport") {
    return "ПТС";
  } else if (str === "personal_passport") {
    return "Паспорт";
  } else if (str === "vehicle_certificate") {
    return "СТС";
  } else {
    return "В/У";
  }
}
