import img85088621 from "figma:asset/b81b4a2f1d6dd33617eaa8d69e28710e079f0b7b.png";

function Frame1() {
  return (
    <div className="absolute bg-[#2b2d30] h-[81px] left-[444px] rounded-[20px] top-[561px] w-[552px]">
      <div className="box-border content-stretch flex gap-[10px] h-[81px] items-center justify-center overflow-clip px-[64px] py-0 rounded-[inherit] w-[552px]" />
      <div aria-hidden="true" className="absolute border-[5px] border-solid inset-0 pointer-events-none rounded-[20px] shadow-[0px_4px_4px_0px_rgba(0,0,0,0.25)]" />
    </div>
  );
}

function Group() {
  return (
    <div className="absolute contents left-[444px] top-[561px]">
      <Frame1 />
      <p className="absolute font-['Average_Sans:Regular',sans-serif] h-[54px] leading-[normal] left-[560.5px] not-italic text-[#dcdee3] text-[36px] text-center top-[573px] tracking-[1.8px] translate-x-[-50%] w-[211px]">{`Ask away: `}</p>
    </div>
  );
}

function Frame2() {
  return (
    <div className="absolute box-border content-stretch flex gap-[10px] h-[374px] items-center justify-center left-[395px] overflow-clip px-[55px] py-[27px] top-[119px] w-[650px]">
      <div className="font-['Bai_Jamjuree:Medium',sans-serif] h-[320px] leading-[70px] not-italic relative shrink-0 text-[48px] text-white tracking-[2.4px] w-[616px]">
        <p className="mb-0">Introducing Ouroboros,</p>
        <p className="mb-0">{`Unparalleled `}</p>
        <p className="mb-0">Tool-Assisted Generative</p>
        <p className="mb-0">AI</p>
        <p>&nbsp;</p>
      </div>
    </div>
  );
}

function Frame3() {
  return (
    <div className="bg-[rgba(11,11,11,0)] box-border content-stretch flex flex-col gap-[8px] items-center justify-center overflow-clip p-[10px] relative shrink-0 w-[46px]">
      <div className="bg-white h-[2.5px] shrink-0 w-[50px]" />
      <div className="bg-white h-[2.5px] shrink-0 w-[50px]" />
      <div className="bg-white h-[2.5px] shrink-0 w-[50px]" />
    </div>
  );
}

function Navbar() {
  return (
    <div className="absolute bg-[rgba(0,0,0,0)] box-border content-stretch flex gap-[35px] h-[108px] items-center justify-center left-0 overflow-clip pl-[1351px] pr-0 py-0 top-0 w-[1440px]" data-name="Navbar">
      <Frame3 />
    </div>
  );
}

function Group1() {
  return (
    <div className="absolute contents left-0 top-0">
      <Navbar />
    </div>
  );
}

export default function Frame() {
  return (
    <div className="relative size-full" style={{ backgroundImage: "url('data:image/svg+xml;utf8,<svg viewBox=\\\'0 0 1440 900\\\' xmlns=\\\'http://www.w3.org/2000/svg\\\' preserveAspectRatio=\\\'none\\\'><rect x=\\\'0\\\' y=\\\'0\\\' height=\\\'100%\\\' width=\\\'100%\\\' fill=\\\'url(%23grad)\\\' opacity=\\\'1\\\'/><defs><radialGradient id=\\\'grad\\\' gradientUnits=\\\'userSpaceOnUse\\\' cx=\\\'0\\\' cy=\\\'0\\\' r=\\\'10\\\' gradientTransform=\\\'matrix(4.4087e-15 45 -72 2.7555e-15 720 450)\\\'><stop stop-color=\\\'rgba(255,255,255,1)\\\' offset=\\\'0\\\'/><stop stop-color=\\\'rgba(203,191,204,1)\\\' offset=\\\'0.25\\\'/><stop stop-color=\\\'rgba(176,160,179,1)\\\' offset=\\\'0.375\\\'/><stop stop-color=\\\'rgba(150,128,154,1)\\\' offset=\\\'0.5\\\'/><stop stop-color=\\\'rgba(119,103,123,1)\\\' offset=\\\'0.625\\\'/><stop stop-color=\\\'rgba(88,78,92,1)\\\' offset=\\\'0.75\\\'/><stop stop-color=\\\'rgba(57,53,61,1)\\\' offset=\\\'0.875\\\'/><stop stop-color=\\\'rgba(42,40,45,1)\\\' offset=\\\'0.9375\\\'/><stop stop-color=\\\'rgba(27,28,29,1)\\\' offset=\\\'1\\\'/></radialGradient></defs></svg>')" }}>
      <Group />
      <div className="absolute h-[98px] left-[18px] pointer-events-none rounded-[20px] top-[7px] w-[102px]" data-name="8508862 1">
        <div className="absolute inset-0 overflow-hidden rounded-[20px]">
          <img alt="" className="absolute h-[283.95%] left-[-19.37%] max-w-none top-[-36.85%] w-[356.78%]" src={img85088621} />
        </div>
        <div aria-hidden="true" className="absolute border-[0.5px] border-solid border-white inset-0 rounded-[20px]" />
      </div>
      <Frame2 />
      <Group1 />
    </div>
  );
}