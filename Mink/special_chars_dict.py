class namespace_dict(dict):
    def __getattr__(self, __name: str):
        try:
            return super().__getattr__(__name)

        except AttributeError:
            return self.__getitem__(__name)


def sup(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)

def sub(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)
    
    
sc = namespace_dict([("lambda","\u03bb")],
          pm="\u00b1",
          alpha="\u03b1",
          beta="\u03b2",
          gamma="\u03b3",
          delta="\u03b4",
          epsilon="\u03b5",
          zeta="\u03b6",
          eta="\u03b7",
          theta="\u03b8",
          iota="\u03b9",
          kappa="\u03ba",
          mu="\u03bc",
          nu="\u03bd",
          xi="\u03be",
          omicron="\u03bf",
          pi="\u03c0",
          rho="\u03c1",
          sigma="\u03c3",
          tau="\u03c4",
          upsilon="\u03c5",
          phi="\u03c6",
          chi="\u03c7",
          psi="\u03c8",
          omega="\u03c9",
          Alpha="\u0391",
          Beta="\u0392",
          Gamma="\u0393",
          Delta="\u0394",
          Epsilon="\u0395",
          Zeta="\u0396",
          Eta="\u0397",
          Theta="\u0398",
          Iota="\u0399",
          Kappa="\u039a",
          Lambda="\u039b",
          Mu="\u039c",
          Nu="\u039d",
          Xi="\u039e",
          Omicron="\u039f",
          Pi="\u03a0",
          Rho="\u03a1",
          Sigma="\u03a3",
          Tau="\u03a4",
          Upsilon="\u03a5",
          Phi="\u03a6",
          Chi="\u03a7",
          Psi="\u03a8",
          Omega="\u03a9",
          angstrom="\u212b",
          degree="\u00b0",
          micro="\u00b5",
          script_l="\u2113",
          prime="\u2032",
          pprime="\u2033"
          )

sc.sub = sub
sc.sup = sup

if __name__ == "__main__":
    print(sc.items())
    print(sc.pm)
    print(sc.zeta)
    print(f"{sc.nu + sc.sup('2') + sc.sub('1')}")