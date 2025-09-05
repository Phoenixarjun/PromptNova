"use client"

import { useRouter } from "next/router";

     const TypeGuidePage = () => {
       const router = useRouter();
       const { slug } = router.query;

       return (
         <div className="min-h-screen bg-white text-black p-6">
           <h1 className="text-3xl font-semibold mb-6 text-gray-900">{slug}</h1>
           <p className="text-gray-600">Detailed guide for {slug} will be added here.</p>
         </div>
       );
     };

     export default TypeGuidePage;