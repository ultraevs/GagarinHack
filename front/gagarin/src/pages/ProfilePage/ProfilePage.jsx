import Documents from "../../components/Documents/Documents";
import DropZone from "../../components/DropZone/DropZone";

const ProfilePage = () => {
  return (
    <section>
      <h2 className="title">Аккаунт <span>/ документы</span></h2>
      <DropZone />
      <Documents />
    </section>
  );
};

export default ProfilePage;
