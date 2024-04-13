import { useState } from "react";
import Documents from "../../components/Documents/Documents";
import DropZone from "../../components/DropZone/DropZone";
import { ThreeDot } from "react-loading-indicators";

const ProfilePage = () => {
  const [loading, setLoading] = useState(false);
  return (
    <section>
      <h2 className="title">
        Аккаунт <span>/ документы</span>
      </h2>
      <DropZone setLoading={setLoading} />
      <div style={{marginTop: 10}}>
        {loading && (
          <ThreeDot color="#ff7250" size="large" text="" textColor="" />
        )}
      </div>
      <Documents />
    </section>
  );
};

export default ProfilePage;
